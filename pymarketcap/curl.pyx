# External cython modules
from libc.stddef cimport size_t
from libc.string cimport memcpy
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

# External C modules
from curl cimport *

# Internal project modules
from pymarketcap.errors import CoinmarketcapHTTPError
from pymarketcap import __version__

# https://curl.haxx.se/libcurl/c/getinmemory.html
cdef struct MemoryStruct:
    char *memory
    size_t size

cdef size_t write_memory(void *contents, size_t size,
                         size_t nmemb, void *userp):
    cdef size_t realsize = size * nmemb
    cdef MemoryStruct *mem = <MemoryStruct *>userp
    mem.memory = <char *>PyMem_Realloc(
        mem.memory, mem.size + realsize + 1
    )
    if mem.memory == NULL:
        print("Not enough memory (realloc returned NULL)\n")
        return 0
    memcpy(&(mem.memory[mem.size]), contents, realsize)
    mem.size += realsize
    mem.memory[mem.size] = 0
    return realsize

cdef class Response(object):
    cdef readonly long status_code
    cdef readonly bytes text
    cdef readonly bytes content_type
    cdef readonly bytes encoding
    cdef readonly bytes url

    def __cinit__(self, text):
        self.text = text

cpdef Response get_to_memory(const char *url, long timeout,
                             bint debug):
    """Send a get request using a buffer stored in memory.

    Args:
        url (char *): A direction in memory of url.
        timeout (long): Number of seconds until expiration
            time cancels the request.
        debug (bint): Flag to activate/desactivate body
            response printing.

    Returns (Response):
        Returns a class with next attributes:
            ``text``, ``status_code``, ``url``.
    """
    cdef CURLcode ret
    cdef long true = 1L
    version = curl_version()
    cdef CURL *curl = curl_easy_init()
    cdef const char *user_agent = "pymarketcap 4.0.009"
    cdef const char *accept_encoding = "gzip, deflate"
    cdef char *raw_body

    cdef MemoryStruct chunk
    chunk.memory = <char *>PyMem_Malloc(1)
    chunk.size = 0

    if curl != NULL:
        if debug:
            curl_easy_setopt(curl, CURLOPT_VERBOSE,
                             &true)
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION,
                         &true)
        ret = curl_easy_setopt(curl, CURLOPT_URL, url)
        ret = curl_easy_setopt(curl, CURLOPT_TIMEOUT,
                               <void *>timeout)

        ret = curl_easy_setopt(curl, CURLOPT_HTTPGET,
                               &true)

        ret = curl_easy_setopt(curl, CURLOPT_USERAGENT,
                               user_agent)
        ret = curl_easy_setopt(curl, CURLOPT_ACCEPT_ENCODING,
                               accept_encoding)

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION,
                         &write_memory)
        curl_easy_setopt(curl, CURLOPT_WRITEDATA,
                         <void *>&chunk)

        if ret != CURLE_OK:
            raise RuntimeError
        ret = curl_easy_perform(curl)
        if ret != CURLE_OK:
            raise CoinmarketcapHTTPError

        resp = Response(chunk.memory)
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE,
                          &resp.status_code)
        curl_easy_cleanup(curl)

        PyMem_Free(chunk.memory)

        return resp
