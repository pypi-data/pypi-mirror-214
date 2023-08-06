var echolocator__PixelUx__UserMotionEvent = "echolocator__PixelUx__UserMotionEvent";
var echolocator__PixelUx__UserChangeEvent = "echolocator__PixelUx__UserChangeEvent";

class echolocator__PixelUx extends echolocator__UxBase {
    UPDATE = "echolocator_guis::commands::update";

    #raphael = null;
    #color = null;
    #is_draggable = null;
    #transformer = null;
    #guide = null;
    #uuid = null;
    #target = null;

    constructor(runtime, plugin_link_name, $interaction_parent, color, is_draggable) {
        super(runtime);

        this.plugin_link_name = plugin_link_name;
        this.$interaction_parent = $interaction_parent;
        this.#color = color;
        this.#is_draggable = is_draggable;
    }

    // -------------------------------------------------------------
    // Activate things on the UX.

    activate(raphael) {
        super.activate()
        this.#raphael = raphael;

        // TODO: Try to use raphael normal transformation instead of transformer class.
        this.#transformer = this.#raphael.webviz_transformer;

        var that = this;

        this.#guide = new webviz__hair__Guide2(this, this.plugin_link_name);

        // Guide is moving.
        this.#guide.addEventListener(
            webviz__hair__Guide2__UserMotionEvent,
            function (event) { that.handle_guide_motion_event(event); });

        // Guide stops.
        this.#guide.addEventListener(
            webviz__hair__Guide2__UserChangeEvent,
            function (event) { that.handle_guide_change_event(event); });

        this.#guide.activate(this.#raphael, this.#color, this.#is_draggable);

        // Set box to appear guaranteed on-screen somewhere.
        this.#guide.set_box({ position: { x: 110, y: 220 }, visible: true });

    } // end method

    // -------------------------------------------------------------
    // When the selected image changes, we get notified.
    // We will move the guide to the image's target location.
    // We will update the x and y as the guid moves.

    enabled(flag) {
        var F = "echolocator__PixelUx[" + this.plugin_link_name + "]::enabled"

        this.#is_draggable = flag;
        this.#guide.set_box({ "enabled": flag });

    } // end method

    // -------------------------------------------------------------
    // When the selected image changes, we get notified.
    // We will move the guide to the image's target location.
    // We will update the x and y as the guid moves.

    set_uuid(uuid, target) {
        var F = "echolocator__PixelUx[" + this.plugin_link_name + "]::set_uuid"

        // Remember the image info.
        this.#uuid = uuid;
        this.#target = target;

        console.log(F + ": uuid " + this.#uuid + " is for target [" + this.#target.x + ", " + this.#target.y + "]")

        this.render();

    } // end method

    // -----------------------------------------------------------------------
    // Render the viewable things according to the current tranformer settings.
    render(event) {
        var F = "echolocator__PixelUx[" + this.plugin_link_name + "]::render"

        // console.log(F + ": [INTERPI] rendering target [" + this.#target.x + ", " + this.#target.y + "]")

        // Everything we send or receive from the outside is data coordinates.
        // Convert it to view coordinates which is are used by the guide.
        var view_position = this.#transformer.data_to_view(this.#target);

        // console.log(F + ": [INTERPI] rendering to view position [" + view_position.x + ", " + view_position.y + "]")

        // Move the guide to the canvas view location.
        this.#guide.set_box({ position: view_position })

    } // end method

    // -----------------------------------------------------------------------
    // Guide is moving (dragging).
    handle_guide_motion_event(event) {
        var F = "echolocator__PixelUx[" + this.plugin_link_name + "]::handle_guide_motion_event"

        // Trigger an event that image_edit.js will use to avoid handling the click on the paper.
        var custom_event = new CustomEvent(echolocator__PixelUx__UserMotionEvent,
            {
                detail: {}
            });

        this.dispatchEvent(custom_event);

    } // end method


    // -----------------------------------------------------------------------
    // Guide has changed (mouse up after dragging).
    // Also can be called by image_edit_ux after click on canvas.
    handle_guide_change_event(event) {
        var F = "echolocator__PixelUx[" + this.plugin_link_name + "]::handle_guide_change_event"

        console.log(F + " guide changed")

        // The guide gives view coordinates.
        var view_position = this.#guide.get().position;

        // Everything we send or receive from the outside is data coordinates.
        this.#target = this.#transformer.view_to_data(view_position)

        console.log(F + ": [INTERPI] dragged view_position" +
            " [" + view_position.x + ", " + view_position.y + "]" +
            " transformed to target" +
            " [" + this.#target.x + ", " + this.#target.y + "]");

        // Trigger an event that image_edit.js will use to save the target and advance to the next image.
        var custom_event = new CustomEvent(echolocator__PixelUx__UserChangeEvent,
            {
                detail: { target: this.#target }
            });

        this.dispatchEvent(custom_event);

    } // end method

}