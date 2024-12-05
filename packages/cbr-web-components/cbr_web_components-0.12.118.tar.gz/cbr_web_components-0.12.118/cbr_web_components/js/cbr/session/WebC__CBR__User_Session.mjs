import Web_Component                from "../../core/Web_Component.mjs"
import CBR__Session__Event__Handler from "./CBR__Session__Event__Handler.mjs"
import CBR__Session__API__Handler   from "./CBR__Session__API__Handler.mjs"
import CBR__Session__State__Manager from "./CBR__Session__State__Manager.mjs"
import Div                          from "../../core/Div.mjs"
import Icon                         from "../../css/icons/Icon.mjs"
import CSS__Badges                  from "../../css/CSS__Badges.mjs"
import CSS__Session                 from "./CSS__Session.mjs"

export default class WebC__CBR__User_Session extends Web_Component {
    constructor() {
        super()
        this.event_handler = new CBR__Session__Event__Handler()
        this.api_handler   = new CBR__Session__API__Handler()
        this.state_manager = new CBR__Session__State__Manager()
        new CSS__Session   (this).apply_framework()
        new CSS__Badges    (this).apply_framework()
    }

    async connectedCallback() {
        await this.load_initial_state()
        super.connectedCallback()
        this.setup_event_listeners()
        this.state_manager.set_initialized()
        this.event_handler.dispatch(this.event_handler.events.SESSION_INITIALIZED,
                                   { state: this.state_manager.get_state() })
    }

    async load_initial_state() {
        try {
            const user_session_id     = this.api_handler.get_user_session_id()
            const persona_session_id  = this.api_handler.get_persona_session_id()
            const active_session_id   = this.api_handler.get_active_session_id()     // Will always exist

            // Load both available sessions and the active session
            const session_promises = []

            if (user_session_id) {
                session_promises.push(
                    this.api_handler.get_session_details(user_session_id)
                        .then(session => this.state_manager.set_user_session(session))
                )
            }

            if (persona_session_id) {
                session_promises.push(
                    this.api_handler.get_session_details(persona_session_id)
                        .then(session => this.state_manager.set_persona_session(session))
                )
            }

            // Always load active session
            session_promises.push(
                this.api_handler.get_session_details(active_session_id)
                    .then(session => this.state_manager.set_active_session(session))
            )

            await Promise.all(session_promises)

        } catch (error) {
            this.state_manager.set_error(error)
            this.event_handler.dispatch(
                this.event_handler.events.SESSION_ERROR,
                { error }
            )
        }
    }

    handle__switch_session = async (event) => {
        const session_id = event.detail.session_id
        try {
            await this.api_handler.set_active_session(session_id)
            const session = await this.api_handler.get_session_details(session_id)
            this.state_manager.set_active_session(session)

            // Re-render the current component
            this.render()

            // Dispatch event for other components
            this.event_handler.dispatch(
                this.event_handler.events.ACTIVE_SESSION_CHANGED,
                {
                    state: this.state_manager.get_state(),
                    session_id: session_id,
                    user_name: session.user_name
                }
            )
        } catch (error) {
            this.state_manager.set_error(error)
            this.event_handler.dispatch(
                this.event_handler.events.SESSION_ERROR,
                { error }
            )
        }
    }


    handle__login_as_persona = async (event) => {
        try {
            await this.api_handler.login_as_persona(event.detail.persona_id)
            await this.load_initial_state()
            this.event_handler.dispatch(
                this.event_handler.events.PERSONA_SESSION_CHANGED,
                { state: this.state_manager.get_state() }
            )
        } catch (error) {
            this.state_manager.set_error(error)
            this.event_handler.dispatch(
                this.event_handler.events.SESSION_ERROR,
                { error }
            )
        }
    }

    handle__logout_persona = async () => {
        try {
            await this.api_handler.logout_persona()
            this.state_manager.clear_persona_session()

            // Switch active session back to user session
            const user_session_id = this.api_handler.get_user_session_id()
            await this.api_handler.set_active_session(user_session_id)
            const user_session = await this.api_handler.get_session_details(user_session_id)
            this.state_manager.set_active_session(user_session)

            // Re-render and notify
            this.render()
            this.event_handler.dispatch( this.event_handler.events.PERSONA_SESSION_CHANGED,
                                        { state: this.state_manager.get_state() })
        } catch (error) {
            this.state_manager.set_error(error)
            this.event_handler.dispatch(
                this.event_handler.events.SESSION_ERROR,
                { error }
            )
        }
    }

    handle__persona_session_changed = async () => {
        await this.load_initial_state()
        this.render()
    }

    setup_event_listeners() {
        this.event_handler.subscribe(this.event_handler.events.LOGIN_AS_PERSONA       , this.handle__login_as_persona       )
        this.event_handler.subscribe(this.event_handler.events.LOGOUT_PERSONA         , this.handle__logout_persona         )
        this.event_handler.subscribe(this.event_handler.events.SWITCH_SESSION         , this.handle__switch_session         )
        this.event_handler.subscribe(this.event_handler.events.PERSONA_SESSION_CHANGED, this.handle__persona_session_changed)
    }

    disconnectedCallback() {
        this.event_handler.unsubscribe_all()
    }

    is_active_session(session) {
        return this.state_manager.get_state().active_session?.user_name === session?.user_name
    }

    render() {
        const state = this.state_manager.get_state()
        const session_indicator = new Div({ class: 'session-indicator'})

        // User session element
        if (state.user_session) {
            const user_session = new Div({
                class: `session-item user ${this.is_active_session(state.user_session) ? 'active' : ''}`,
                attributes: {
                    'data-session-id': this.api_handler.get_user_session_id(),
                    'data-session-type': 'user'
                }
            })
            const user_icon    = new Icon({ class: 'session-icon'   , icon: 'user'                            })
            const user_text    = new Div ({ class: 'session-text'   , value: state.user_session.user_name     })
            const user_badge   = new Div ({ class: `badge badge-pill ${this.is_active_session(state.user_session) ? 
                                                                      'badge-success' : 'badge-secondary'}`,
                                          value: 'User'                                                        })

            user_session.add_elements(user_icon, user_text, user_badge)
            session_indicator.add_element(user_session)
        }

        // Persona session element (if active)
        if (state.persona_session) {
            const persona_session = new Div({
                class: `session-item persona ${this.is_active_session(state.persona_session) ? 'active' : ''}`,
                attributes: {
                    'data-session-id': this.api_handler.get_persona_session_id(),
                    'data-session-type': 'persona'
                }
            })
            const persona_icon    = new Icon({ class: 'session-icon'  , icon: 'person'                        })
            const persona_text    = new Div ({ class: 'session-text'  , value: state.persona_session.user_name})
            const persona_badge   = new Div ({ class: `badge badge-pill ${this.is_active_session(state.persona_session) ? 
                                                                         'badge-success' : 'badge-secondary'}`,
                                             value: 'Persona'                                                 })
            const revert_icon     = new Icon({ class: 'revert-icon'   , icon: 'logout',
                                             attributes: { 'data-action': 'revert' }                          })

            persona_session.add_elements(persona_icon, persona_text, persona_badge)
            persona_session.add_element(revert_icon)
            session_indicator.add_element(persona_session)
        }

        this.set_inner_html(session_indicator.html())

        // Add DOM event listeners after HTML is set
        this.setup_dom_events()
    }

    setup_dom_events() {
        const session_items = this.query_selector_all('.session-item')
        session_items.forEach(item => {
            item.addEventListener('click', (event) => {
                const session_id = item.dataset.sessionId
                if (session_id) {
                    this.event_handler.dispatch(
                        this.event_handler.events.SWITCH_SESSION,
                        { session_id: session_id }
                    )
                }
            })
        })

        const revert_icon = this.query_selector('[data-action="revert"]')
        if (revert_icon) {
            revert_icon.addEventListener('click', (event) => {
                event.stopPropagation() // Prevent triggering session switch
                this.event_handler.dispatch(this.event_handler.events.LOGOUT_PERSONA)
            })
        }
    }
}

WebC__CBR__User_Session.define()