"""Holds constant that are related to HTML documents"""


class Events:
    # More events can be found at https://www.w3schools.com/tags/ref_eventattributes.asp

    # Window Events
    # -------------
    afterprint = 'afterprint'  # Script to be run after the document is printed
    beforeprint = 'beforeprint'  # Script to be run before the document is printed
    beforeunload = 'beforeunload'  # Script to be run when the document is about to be unloaded
    error = 'error'  # Script to be run when an error occurs
    hashchange = 'hashchange'  # Script to be run when there has been changes to the anchor part of the
    load = 'load'  # Fires after the page is finished loading
    message = 'message'  # Script to be run when the message is triggered
    offline = 'offline'  # Script to be run when the browser starts to work offline
    online = 'online'  # Script to be run when the browser starts to work online
    pagehide = 'pagehide'  # Script to be run when a user navigates away from a page
    pageshow = 'pageshow'  # Script to be run when a user navigates to a page
    popstate = 'popstate'  # Script to be run when the window's history changes
    resize = 'resize'  # Fires when the browser window is resized
    storage = 'storage'  # Script to be run when a Web Storage area is updated
    unload = 'unload'  # Fires once a page has unloaded (or the browser window has been closed)

    # Form Events
    # -----------
    blur = 'blur'  # Fires the moment that the element loses focus
    change = 'change'  # Fires the moment when the value of the element is changed
    contextmenu = 'contextmenu'  # Script to be run when a context menu is triggered
    focus = 'focus'  # Fires the moment when the element gets focus
    input = 'input'  # Script to be run when an element gets user input
    invalid = 'invalid'  # Script to be run when an element is invalid
    reset = 'reset'  # Fires when the Reset button in a form is clicked
    search = 'search'  # Fires when the user writes something in a search field (for <input="search">)
    select = 'select'  # Fires after some text has been selected in an element
    submit = 'submit'  # Fires when a form is submitted

    # Keyboard Events
    # ---------------
    keydown = 'keydown'  # Fires when a user is pressing a key
    keypress = 'keypress'  # Fires when a user presses a key
    keyup = 'keyup'  # Fires when a user releases a key
