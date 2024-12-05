export class Mock_Fetch {
    constructor() {
        this.responses = new Map()
    }

    static apply_mock(target_class) {                                    // Much simpler now - just patch and go
        target_class.prototype.fetch_url = function(...args) {
            return mock.fetch_url.apply(mock, args)
        }
        return mock
    }

    static restore_original(target_class, original) {                    // Optional restore if needed
        if (original) {
            target_class.prototype.fetch_url = original
        }
    }

    async fetch_url(url) {
        if (!this.responses.has(url)) {
            throw new Error(`No mock response set for URL: ${url}`)
        }

        const response = this.responses.get(url)
        return {
            ok     : response.status === 200   ,
            status : response.status || 200    ,
            json   : async () => response.data ,
            body   : response.body             ,
            headers: response.headers || {}
        }
    }

    set_response(url, data, status = 200) {
        this.responses.set(url, { data, status })
    }

    set_stream_response(url, chunks, status = 200) {
        this.responses.set(url, { ok: status === 200              ,
                                  status                          ,
                                  body: new StreamResponse(chunks)});
    }
}

export const mock = new Mock_Fetch()                                    // Single instance for convenience

export function set_mock_response(url, data, status = 200) {           // Helper function
    mock.set_response(url, data, status)
}

class StreamResponse {
    constructor(chunks) {
        this.chunks = Array.isArray(chunks) ? chunks : [chunks];
        this.encoder = new TextEncoder();
    }

    getReader() {
        let index = 0;
        return {
            read: async () => {
                if (index >= this.chunks.length) {
                    return { done: true };
                }
                return {
                    value: this.encoder.encode(this.chunks[index++]),
                    done: false
                };
            }
        };
    }
}