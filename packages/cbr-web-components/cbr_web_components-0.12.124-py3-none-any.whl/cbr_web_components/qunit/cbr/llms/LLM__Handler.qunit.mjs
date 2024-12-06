import LLM__Handler                                 from '../../../js/cbr/llms/LLM__Handler.mjs'
import { Mock_Fetch }                               from '../api/Mock_Fetch.mjs'
import { setup_mock_responses, set_mock_response }  from '../api/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_USER_PROMPT     = 'test prompt'
const MOCK_SYSTEM_PROMPTS  = ['system prompt 1', 'system prompt 2']
const MOCK_STREAM_RESPONSE = 'Hello World!'

module('LLM__Handler', hooks => {
    let handler
    let original_fetch_url
    let mock_fetch
    let original_console_error

    hooks.beforeEach(() => {
        setup_mock_responses()
        original_console_error = console.error
        console.error = () => {}

        handler = new LLM__Handler()
        mock_fetch = Mock_Fetch.apply_mock(LLM__Handler)
    })

    hooks.afterEach(() => {
        Mock_Fetch.restore_original(LLM__Handler, original_fetch_url)
        console.error = original_console_error
    })

    test('fetch_url sends correct request', async assert => {
        const test_path = '/test/path'
        const test_payload = { key: 'value' }

        mock_fetch.set_response(test_path, test_payload)
        const response = await handler.fetch_url(test_path, test_payload)

        assert.ok(response.ok                                                      , 'Response is successful')
        assert.equal(response.status                    , 200                      , 'Status is 200')
        assert.deepEqual(await response.json()          , test_payload             , 'Returns correct data')
    })

    test('fetch_url handles errors', async assert => {
        const test_path = '/error/path'
        mock_fetch.set_response(test_path, {}, 500)

        const response = await handler.fetch_url(test_path, {})
        assert.notOk(response.ok                                                   , 'Response shows error')
        assert.equal(response.status                    , 500                      , 'Status is 500')
    })

    // Previous constructor, payload and uuid tests remain unchanged
    test('stream_response handles successful stream', async assert => {
        const chunks = ['Hello', ' World', '!'];

        mock_fetch.set_stream_response(handler.api_path, chunks);

        const received_chunks = [];

        const result = await handler.stream_response(
            MOCK_USER_PROMPT,
            MOCK_SYSTEM_PROMPTS,
            { onChunk: chunk => received_chunks.push(chunk) });

        assert.equal(result, 'Hello World!');
        assert.deepEqual(received_chunks, ['Hello', 'Hello World', 'Hello World!']);
    });

    test('stream_response handles errors', async assert => {
        handler.fetch_url = async () => { throw new Error('Network error') }

        const error_callback = (error) => {
            assert.equal(error.message, 'Network error'              , 'Error callback received')
        }

        try {
            await handler.stream_response(MOCK_USER_PROMPT, MOCK_SYSTEM_PROMPTS, { onError: error_callback })
            assert.notOk(true                                       , 'Should throw error')
        } catch (error) {
            assert.equal(error.message, 'Network error'              , 'Throws network error')
        }
    })
})