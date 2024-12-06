import WebC__Target_Div          from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component             from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Actions from '../../../js/cbr/file-system/WebC__User_Files__Actions.mjs'
import { setup_mock_responses, set_mock_response } from '../api/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_FOLDER_DATA = {
    node_id: 'test-folder-123',
    name   : 'Test Folder'
}

module('WebC__User_Files__Actions', hooks => {
    let target_div
    let actions
    let api_calls = []

    hooks.beforeEach(async () => {
        setup_mock_responses()

        // Track API calls
        api_calls = []
        set_mock_response('/api/user-data/files/add-folder'                               , 'POST'  , { success: true })
        set_mock_response('/api/user-data/files/add-file'                                 , 'POST'  , { success: true })
        set_mock_response('/api/user-data/files/folder-rename'                            , 'POST'  , { success: true })
        set_mock_response('/api/user-data/files/delete-folder'                            , 'DELETE', { success: true })
        set_mock_response('/api/user-data/files/delete-folder?folder_id=test-folder-123'  , 'DELETE', { success: true })

        target_div = WebC__Target_Div.add_to_body()
        actions = await target_div.append_child(WebC__User_Files__Actions)
        await actions.wait_for__component_ready()
    })

    hooks.afterEach(() => {
        actions.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        // Test component registration and naming
        assert.equal(actions.tagName.toLowerCase()        , 'webc-user-files-actions', 'Has correct tag name'     )
        assert.equal(actions.constructor.element_name     , 'webc-user-files-actions', 'Has correct element name' )
        assert.equal(actions.constructor.name             , 'WebC__User_Files__Actions', 'Has correct class name' )

        // Test shadow DOM and API
        assert.ok(actions.shadowRoot                                                  , 'Has shadow root'         )
        assert.ok(actions.api_invoke                                                  , 'Has API__Invoke'        )

        // Test inheritance
        assert.ok(actions instanceof Web_Component                                    , 'Extends Web_Component'   )
        assert.ok(actions instanceof HTMLElement                                      , 'Is HTML Element'         )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = actions.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                  , 'Has CSS rules'           )
        assert.ok(css_rules['.actions-container']                                    , 'Has container styles'    )
        assert.ok(css_rules['.folder-info']                                         , 'Has folder info styles'  )
        assert.ok(css_rules['.action-button']                                       , 'Has button styles'       )
    })

    test('renders initial state correctly', async assert => {
        // Test container structure
        const container = actions.query_selector('.actions-container')
        assert.ok(container                                                          , 'Container exists'        )

        // Test folder info section
        const folder_info = actions.query_selector('.folder-info')
        assert.ok(folder_info                                                        , 'Folder info exists'      )
        assert.ok(folder_info.textContent.includes('root')                          , 'Shows root folder'       )

        // Test form elements
        assert.ok(actions.query_selector('.new-folder-input')                       , 'New folder input exists' )
        assert.ok(actions.query_selector('.new-markdown-input')                     , 'Markdown input exists'   )
        assert.ok(actions.query_selector('.new-folder-btn')                         , 'Add folder button exists')
        assert.ok(actions.query_selector('.new-markdown-btn')                       , 'Add markdown button exists')
    })

    test('handles folder selection', async assert => {
        // Simulate folder selection
        const folder_event = new CustomEvent('folder-selected', {
            detail: MOCK_FOLDER_DATA
        })
        document.dispatchEvent(folder_event)
        await actions.wait_for(100)  // Wait for render

        const folder_name = actions.query_selector('.folder-name')
        assert.equal(folder_name.textContent                     , 'Test Folder'    , 'Updates folder name'     )

        // Test rename/delete elements appear
        assert.ok(actions.query_selector('.rename-input')                           , 'Rename input appears'    )
        assert.ok(actions.query_selector('.action-button.rename')                   , 'Rename button appears'   )
        assert.ok(actions.query_selector('.action-button.delete')                   , 'Delete button appears'   )
    })

    test('adds new folder', async assert => {
        const input = actions.query_selector('.new-folder-input')
        const button = actions.query_selector('.new-folder-btn')

        input.value = 'New Test Folder'
        button.click()

        assert.expect(1)

        actions.addEventListener('files-refresh', () => {
            assert.ok(true                                                          , 'Triggers refresh event'  )
        })
    })

    test('creates markdown file', async assert => {
        const input = actions.query_selector('.new-markdown-input')
        const button = actions.query_selector('.new-markdown-btn')

        input.value = 'test-doc.md'
        button.click()

        assert.expect(1)

        actions.addEventListener('files-refresh', () => {
            assert.ok(true                                                          , 'Triggers refresh event'  )
        })
    })

    test('handles rename operation', async assert => {
        // Setup folder selection first
        document.dispatchEvent(new CustomEvent('folder-selected', {
            detail: MOCK_FOLDER_DATA
        }))
        await actions.wait_for(100)

        const input = actions.query_selector('.rename-input')
        const button = actions.query_selector('.action-button.rename')

        input.value = 'Renamed Folder'
        button.click()

        assert.expect(1)

        actions.addEventListener('files-refresh', () => {
            assert.ok(true                                                          , 'Triggers refresh event'  )
        })
    })

    test('handles delete operation', async assert => {
        // Setup folder selection first
        document.dispatchEvent(new CustomEvent('folder-selected', {
            detail: MOCK_FOLDER_DATA
        }))
        await actions.wait_for(100)

        // Mock confirm to return true
        const original_confirm = window.confirm
        window.confirm = () => true

        const delete_button = actions.query_selector('.action-button.delete')
        delete_button.click()

        assert.expect(1)

        actions.addEventListener('files-refresh', () => {
            assert.ok(true                                                          , 'Triggers refresh event'  )
        })

        // Restore original confirm
        window.confirm = original_confirm
    })

    test('prevents root folder operations', async assert => {
        // Setup root folder
        actions.current_folder = {
            node_id: null,
            name   : 'root'
        }
        actions.render()

        assert.notOk(actions.query_selector('.action-button.rename')               , 'No rename button for root')
        assert.notOk(actions.query_selector('.action-button.delete')               , 'No delete button for root')
    })

    test('appends .md extension if needed', async assert => {
        const input = actions.query_selector('.new-markdown-input')
        const button = actions.query_selector('.new-markdown-btn')

        input.value = 'test-doc'  // No extension
        button.click()

        assert.expect(1)

        actions.addEventListener('files-refresh', () => {
            assert.ok(true                                                          , 'Adds .md and refreshes'  )
        })
    })

    test('handles API errors gracefully', async assert => {
        // Mock console.error to prevent actual console output
        const original_console_error = console.error
        console.error = () => {}

        // Setup error responses
        set_mock_response('/api/user-data/files/add-folder', 'POST', null, 500)

        const input = actions.query_selector('.new-folder-input')
        const button = actions.query_selector('.new-folder-btn')

        input.value = 'Error Test'
        button.click()

        await actions.wait_for(100)

        assert.ok(true                                                             , 'Handles error without crashing')

        // Restore console.error
        console.error = original_console_error
    })

     test('logs errors when deleting folder fails', async assert => {
        // Track console.error calls
        const error_logs = []
        const original_console_error = console.error
        console.error = (...args) => error_logs.push(args)

        // Setup folder and error response
        actions.current_folder = MOCK_FOLDER_DATA
        set_mock_response('/api/user-data/files/delete-folder?folder_id=test-folder-123', 'DELETE', null, 500)

        // Mock confirm to return true
        const original_confirm = window.confirm
        window.confirm = () => true

        // Attempt delete
        await actions.delete_current_folder()

        // Verify error was logged
        assert.equal(error_logs.length                     , 1                     , 'Logs one error'          )
        assert.equal(error_logs[0][0]                      , 'Error deleting folder:', 'Correct error message' )
        assert.ok(error_logs[0][1] instanceof Error                                , 'Includes error object'   )

        // Restore mocks
        console.error = original_console_error
        window.confirm = original_confirm
    })

    test('logs errors when renaming folder fails', async assert => {
        // Track console.error calls
        const error_logs = []
        const original_console_error = console.error
        console.error = (...args) => error_logs.push(args)

        // Setup folder and error response
        actions.current_folder = MOCK_FOLDER_DATA
        set_mock_response('/api/user-data/files/folder-rename', 'POST', null, 500)

        // Attempt rename
        await actions.rename_current_folder('new name')

        // Verify error was logged
        assert.equal(error_logs.length                     , 1                     , 'Logs one error'          )
        assert.equal(error_logs[0][0]                      , 'Error renaming folder:', 'Correct error message' )
        assert.ok(error_logs[0][1] instanceof Error                                , 'Includes error object'   )

        // Restore mock
        console.error = original_console_error
    })

    test('prevents operations on root folder', async assert => {
        // Mock alert to track calls
        const alert_messages = []
        const original_alert = window.alert
        window.alert = (msg) => alert_messages.push(msg)

        // Attempt operations on root folder
        actions.current_folder = { node_id: null, name: 'root' }

        await actions.delete_current_folder()
        assert.equal(alert_messages[0]                     , 'Cannot delete root folder', 'Shows delete alert' )

        await actions.rename_current_folder('new name')
        assert.equal(alert_messages[1]                     , 'Cannot rename root folder', 'Shows rename alert' )

        // Restore mock
        window.alert = original_alert
    })


})