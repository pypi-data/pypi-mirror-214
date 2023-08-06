from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredFileLoader
import datetime
from typing import List, Tuple
from langchain.docstore.document import Document
import numpy as np
from tqdm import tqdm
from pypinyin import lazy_pinyin
from ..configs.model_config import *
from ..textsplitter import ChineseTextSplitter

def torch_gc():
    import torch
    if torch.cuda.is_available():
        # with torch.cuda.device(DEVICE):
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    elif torch.backends.mps.is_available():
        try:
            from torch.mps import empty_cache
            empty_cache()
        except Exception as e:
            print(e)
            print("如果您使用的是 macOS 建议将 pytorch 版本升级至 2.0.0 或更高版本，以支持及时清理 torch 产生的内存占用。")



def load_file(filepath, sentence_size=SENTENCE_SIZE):
    loader = UnstructuredFileLoader(filepath, mode="elements")
    textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
    docs = loader.load_and_split(text_splitter=textsplitter)
    # write_check_file(filepath, docs)
    return docs


def write_check_file(filepath, docs):
    folder_path = os.path.join(os.path.dirname(filepath), "tmp_files")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    fp = os.path.join(folder_path, 'load_file.txt')
    fout = open(fp, 'a')
    fout.write("filepath=%s,len=%s" % (filepath, len(docs)))
    fout.write('\n')
    for i in docs:
        fout.write(str(i))
        fout.write('\n')
    fout.close()


def generate_prompt(related_docs: List[str], query: str,
                    prompt_template=PROMPT_TEMPLATE) -> str:
    context = "\n".join([doc.page_content for doc in related_docs])
    prompt = prompt_template.replace("{question}", query).replace("{context}", context)
    return prompt


def seperate_list(ls: List[int]) -> List[List[int]]:
    lists = []
    ls1 = [ls[0]]
    for i in range(1, len(ls)):
        if ls[i - 1] + 1 == ls[i]:
            ls1.append(ls[i])
        else:
            lists.append(ls1)
            ls1 = [ls[i]]
    lists.append(ls1)
    return lists


def similarity_search_with_score_by_vector(
        self, embedding: List[float], k: int = 4
) -> List[Tuple[Document, float]]:
    scores, indices = self.index.search(np.array([embedding], dtype=np.float32), k)
    docs = []
    id_set = set()
    store_len = len(self.index_to_docstore_id)
    for j, i in enumerate(indices[0]):
        if i == -1 or 0 < self.score_threshold < scores[0][j]:
            # This happens when not enough docs are returned.
            continue
        _id = self.index_to_docstore_id[i]
        doc = self.docstore.search(_id)
        if not self.chunk_conent:
            if not isinstance(doc, Document):
                raise ValueError(f"Could not find document for id {_id}, got {doc}")
            doc.metadata["score"] = int(scores[0][j])
            docs.append(doc)
            continue
        id_set.add(i)
        docs_len = len(doc.page_content)
        for k in range(1, max(i, store_len - i)):
            break_flag = False
            for l in [i + k, i - k]:
                if 0 <= l < len(self.index_to_docstore_id):
                    _id0 = self.index_to_docstore_id[l]
                    doc0 = self.docstore.search(_id0)
                    if docs_len + len(doc0.page_content) > self.chunk_size:
                        break_flag = True
                        break
                    elif doc0.metadata["source"] == doc.metadata["source"]:
                        docs_len += len(doc0.page_content)
                        id_set.add(l)
            if break_flag:
                break
    if not self.chunk_conent:
        return docs
    if len(id_set) == 0 and self.score_threshold > 0:
        return []
    id_list = sorted(list(id_set))
    id_lists = seperate_list(id_list)
    for id_seq in id_lists:
        for id in id_seq:
            if id == id_seq[0]:
                _id = self.index_to_docstore_id[id]
                doc = self.docstore.search(_id)
            else:
                _id0 = self.index_to_docstore_id[id]
                doc0 = self.docstore.search(_id0)
                doc.page_content += " " + doc0.page_content
        if not isinstance(doc, Document):
            raise ValueError(f"Could not find document for id {_id}, got {doc}")
        doc_score = min([scores[0][id] for id in [indices[0].tolist().index(i) for i in id_seq if i in indices[0]]])
        doc.metadata["score"] = int(doc_score)
        docs.append(doc)
    torch_gc()
    return docs


class LocalDocQA:
    llm: object = None
    embeddings: object = None
    top_k: int = VECTOR_SEARCH_TOP_K
    chunk_size: int = CHUNK_SIZE
    chunk_conent: bool = True
    score_threshold: int = VECTOR_SEARCH_SCORE_THRESHOLD

    def init_cfg(self,
                 embedding_model: str = EMBEDDING_MODEL,
                 embedding_device=EMBEDDING_DEVICE,
                 llm_history_len: int = LLM_HISTORY_LEN,
                 llm_model: str = LLM_MODEL,
                 llm_device=LLM_DEVICE,
                 top_k=VECTOR_SEARCH_TOP_K,
                 use_ptuning_v2: bool = USE_PTUNING_V2,
                 use_lora: bool = USE_LORA,
                 ):

        self.llm = None
        self.top_k = top_k

    def init_knowledge_vector_store(self,
                                    filepath: str or List[str],
                                    vs_path: str or os.PathLike = None,
                                    sentence_size=SENTENCE_SIZE,
                                    text2vec=None):
        loaded_files = []
        failed_files = []
        if isinstance(filepath, str):
            if not os.path.exists(filepath):
                print("路径不存在")
                return None
            elif os.path.isfile(filepath):
                file = os.path.split(filepath)[-1]
                try:
                    docs = load_file(filepath, sentence_size)
                    print(f"{file} 已成功加载")
                    loaded_files.append(filepath)
                except Exception as e:
                    print(e)
                    print(f"{file} 未能成功加载")
                    return None
            elif os.path.isdir(filepath):
                docs = []
                for file in tqdm(os.listdir(filepath), desc="加载文件"):
                    fullfilepath = os.path.join(filepath, file)
                    try:
                        docs += load_file(fullfilepath, sentence_size)
                        loaded_files.append(fullfilepath)
                    except Exception as e:
                        print(e)
                        failed_files.append(file)

                if len(failed_files) > 0:
                    print("以下文件未能成功加载：")
                    for file in failed_files:
                        print(f"{file}\n")

        else:
            docs = []
            for file in filepath:
                try:
                    docs += load_file(file)
                    print(f"{file} 已成功加载")
                    loaded_files.append(file)
                except Exception as e:
                    print(e)
                    print(f"{file} 未能成功加载")

        if len(docs) > 0:
            print("文件加载完毕，正在生成向量库")
            if vs_path and os.path.isdir(vs_path):
                self.vector_store = FAISS.load_local(vs_path, text2vec)
                self.vector_store.add_documents(docs)
                torch_gc()
            else:
                if not vs_path: assert False
                self.vector_store = FAISS.from_documents(docs, text2vec)  # docs 为Document列表
                torch_gc()

            self.vector_store.save_local(vs_path)
            return vs_path, loaded_files
        else:
            self.vector_store = FAISS.load_local(vs_path, text2vec)
            torch_gc()
            return vs_path, loaded_files
        
    def get_loaded_file(self):
        ds = self.vector_store.docstore
        return set([ds._dict[k].metadata['source'].split(UPLOAD_ROOT_PATH)[-1] for k in ds._dict])


    # query      查询内容
    # vs_path    知识库路径
    # chunk_conent   是否启用上下文关联
    # score_threshold    搜索匹配score阈值
    # vector_search_top_k   搜索知识库内容条数，默认搜索5条结果
    # chunk_sizes    匹配单段内容的连接上下文长度
    def get_knowledge_based_conent_test(self, query, vs_path, chunk_conent,
                                        score_threshold=VECTOR_SEARCH_SCORE_THRESHOLD,
                                        vector_search_top_k=VECTOR_SEARCH_TOP_K, chunk_size=CHUNK_SIZE,
                                        text2vec=None):
        self.vector_store = FAISS.load_local(vs_path, text2vec)
        self.vector_store.chunk_conent = chunk_conent
        self.vector_store.score_threshold = score_threshold
        self.vector_store.chunk_size = chunk_size

        embedding = self.vector_store.embedding_function(query)
        related_docs_with_score = similarity_search_with_score_by_vector(self.vector_store, embedding, k=vector_search_top_k)

        if not related_docs_with_score:
            response = {"query": query,
                        "source_documents": []}
            return response, ""
        torch_gc()
        # prompt = f"{query}. You should answer this question using information from following documents: \n\n"
        prompt = f"{query}. 你必须利用以下文档中包含的信息回答这个问题: \n\n---\n\n"
        prompt += "\n\n".join([f"({k}): " + doc.page_content for k, doc in enumerate(related_docs_with_score)])
        prompt += "\n\n---\n\n"
        prompt = prompt.encode('utf-8', 'ignore').decode()   # avoid reading non-utf8 chars
        # print(prompt)
        response = {"query": query, "source_documents": related_docs_with_score}
        return response, prompt


