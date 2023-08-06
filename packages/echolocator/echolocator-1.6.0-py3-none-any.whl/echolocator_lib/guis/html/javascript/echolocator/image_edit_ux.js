// Class backing the actions ux.

class echolocator__ImageEditUx extends echolocator__UxAutoUpdate {
    COOKIE_NAME = "IMAGE_EDIT_UX";
    FETCH_IMAGE = "echolocator_guis::commands::fetch_image";
    UPDATE = "echolocator_guis::commands::update";
    CRYSTAL_WELL_INDEX = "echolocator_guis::keywords::crystal_well_index";
    CRYSTAL_WELL_INDEX_NEXT = "echolocator_guis::keywords::crystal_well_index_next";
    CRYSTAL_WELL_COUNT = "echolocator_guis::keywords::crystal_well_count";
    SHOULD_ADVANCE = "echolocator_guis::keywords::should_advance";

    #jquery_objects = {};
    #crystal_well_index = null;
    #crystal_well_count = null;
    #record = null;
    #raphael = null;
    #is_dragging = null;
    #transformer = null;
    #confirmed_target_ux = null;
    #well_centroid_ux = null;


    constructor(runtime, plugin_link_name, $interaction_parent) {
        super(runtime);

        this.plugin_link_name = plugin_link_name;
        this.$interaction_parent = $interaction_parent;
    }

    // -------------------------------------------------------------
    // Activate things on the UX.

    activate() {
        var F = "echolocator__ImageEditUx::activate"
        super.activate()

        // Make a spreader which reacts to resizing of the window.
        this.image1_spreader = new webviz__Spreader(this);

        // Make a raphael drawing object.
        // TODO: Make Raphael drawing object big enough for future jumbo-size images.
        this.#raphael = Raphael("raphael1_paper", 4000, 4000);

        this.#is_dragging = false;

        // For transforming coordinates between data and view.
        this.#transformer = new webviz__Transformer(this.runtime);

        // Pass this transformer to anyone who wants to use the raphael for drawing.
        this.#raphael.webviz_transformer = this.#transformer;

        this.#jquery_objects.$raphael1_paper = $("#raphael1_paper SVG", this.$interaction_parent);
        this.#jquery_objects.$image = $("IMG", this.$interaction_parent);
        this.#jquery_objects.$hide_when_no_image = $(".T_hide_when_no_image", this.$interaction_parent);
        this.#jquery_objects.$filename = $(".T_filename", this.$interaction_parent);
        this.#jquery_objects.$crystal_well_index = $(".T_crystal_well_index", this.$interaction_parent);
        this.#jquery_objects.$crystal_well_count = $(".T_crystal_well_count", this.$interaction_parent);
        this.#jquery_objects.$number_of_crystals = $(".T_number_of_crystals", this.$interaction_parent);
        this.#jquery_objects.$is_usable = $(".T_is_usable", this.$interaction_parent);
        this.#jquery_objects.$is_exported_to_soakdb3 = $(".T_is_exported_to_soakdb3", this.$interaction_parent);

        this.#jquery_objects.previous_button = $(".T_previous_button", this.$interaction_parent);
        this.#jquery_objects.accept_button = $(".T_accept_button", this.$interaction_parent);
        this.#jquery_objects.reject_button = $(".T_reject_button", this.$interaction_parent);
        this.#jquery_objects.reset_button = $(".T_reset_button", this.$interaction_parent);
        this.#jquery_objects.next_button = $(".T_next_button", this.$interaction_parent);

        console.log(F + ": raphael1_paper is a " + this.selector_description(this.#jquery_objects.$raphael1_paper))
        var that = this;

        // Window size changes.
        this.image1_spreader.addEventListener(
            webviz__Spreader__SpreadEvent,
            function (event) { that.handle_spread_event(event); });

        // A click on the "paper" <div> sets the target location, unless dragging.
        this.#jquery_objects.$raphael1_paper.click(
            function (jquery_event_object) {
                if (!that.#is_dragging)
                    that._handle_canvas_left_click(jquery_event_object);
            });

        // Disable context menu for right-click on the image.
        this.#jquery_objects.$raphael1_paper.contextmenu(function (jquery_event_object) {
            that._handle_canvas_right_click(jquery_event_object);
            return false;
        });

        // Key down anywhere in the tab.
        this.$interaction_parent.on("keydown", function (jquery_event_object) {
            // Don't pass the event onward, such as allowing the Tab key to select an element in the tab.
            if (jquery_event_object.keyCode === 9) {
                jquery_event_object.preventDefault();
            }

            console.log(F + ": [KYDOEV]" +
                " jquery_event_object.keyCode " + jquery_event_object.keyCode +
                " jquery_event_object.target " + that.node_description(jquery_event_object.target));

            // Left arrow?
            if (jquery_event_object.keyCode === 37) {
                that._handle_previous_or_next(-1);
            }
            // Space bar?
            if (jquery_event_object.keyCode === 32) {
                that._send_update(true);
            }
            // X key?
            if (jquery_event_object.keyCode === 88) {
                that._send_update(false);
            }
            // - key?
            if (jquery_event_object.keyCode === 189) {
                that._send_update(null);
            }
            // Right arrow?
            if (jquery_event_object.keyCode === 39) {
                that._handle_previous_or_next(1);
            }
        });

        // Set up jquery event handling for DOM elements.
        this.#jquery_objects.previous_button.click(
            function (jquery_event_object) {
                console.log(F + ": clicked previous");
                that._handle_previous_or_next(-1);
            });

        this.#jquery_objects.accept_button.click(
            function (jquery_event_object) {
                console.log(F + ": clicked accept");
                that._send_update(true);
            });

        this.#jquery_objects.reject_button.click(
            function (jquery_event_object) {
                console.log(F + ": clicked reject");
                that._send_update(false);
            });

        this.#jquery_objects.reset_button.click(
            function (jquery_event_object) {
                console.log(F + ": clicked undecided");
                that._send_update(null);
            });

        this.#jquery_objects.next_button.click(
            function (jquery_event_object) {
                console.log(F + ": clicked next");
                that._handle_previous_or_next(1);
            });


        // ----------------------------------------------------------
        // Make the draggable crosshair for the target location.
        this.#confirmed_target_ux = new echolocator__PixelUx(
            self.runtime,
            "confirmed_target",
            this.$interaction_parent,
            "yellowgreen",
            true);

        // Handle when user has finished moving the crosshair, event comes from pixel_ux widget.
        this.#confirmed_target_ux.addEventListener(
            echolocator__PixelUx__UserChangeEvent,
            function (event) { that._handle_confirmed_target_ux_change_event(event); that.#is_dragging = false; });

        // Handle when user is moving the crosshair.
        this.#confirmed_target_ux.addEventListener(
            echolocator__PixelUx__UserMotionEvent,
            function (event) { that.#is_dragging = true; });

        // ----------------------------------------------------------
        // Make the crosshair for the well centroid, but it is not draggable.
        this.#well_centroid_ux = new echolocator__CentroidUx(
            self.runtime,
            "well_centroid",
            this.$interaction_parent,
            "lightblue",
            false);

        // ----------------------------------------------------------

        // Activate the spreader to react on window size changes.
        this.image1_spreader.activate($("#image1"), window);

        // Activate well_centroid first, so it lies "under" the confirmed target in case they overlap.
        this.#well_centroid_ux.activate(this.#raphael);
        this.#confirmed_target_ux.activate(this.#raphael);

        // this.request_update()
    } // end method


    // -------------------------------------------------------------
    // When the selected filename changes, we get notified.
    // We will load the image into the display.

    set_crystal_well_index(crystal_well_index) {
        var F = "echolocator__ImageEditUx::set_crystal_well_index";

        console.log(F + ": [CWINDX] crystal_well_index is " + crystal_well_index)

        // Remember the image info.
        this.#crystal_well_index = crystal_well_index;

        // if (this.#crystal_well_index === undefined) {
        //     this.display_ajax_error("there are no more images to view");
        // }
        // else {
        //     this.display_ajax_error(null);

        //     // Request image info from the server.
        //     this.request_update()

        // }

    } // end method

    // -------------------------------------------------------------
    // Send update to currently loaded image.

    _send_update(is_usable, confirmed_target) {
        var F = "echolocator__ImageEditUx::_handle_is_usable_change";

        if (this.#crystal_well_index !== null && this.#crystal_well_index !== undefined) {
            // Build json request.
            var json_object = {}
            // TODO: Remove hardcoded "IMAGE_LIST_UX" in image edit's cookie list.
            json_object[this.ENABLE_COOKIES] = [this.COOKIE_NAME, "IMAGE_LIST_UX"]
            json_object[this.COMMAND] = this.UPDATE;

            // We pass the fields of the database we want updated.
            var model =
            {
                "crystal_well_uuid": this.#record.uuid,
                "is_usable": is_usable
            }

            if (confirmed_target !== undefined) {
                model["confirmed_target_x"] = confirmed_target.x;
                model["confirmed_target_y"] = confirmed_target.y;
            }
            // Caller is confirming the drop target?
            else if (is_usable === true) {
                // But no previous drop target has been set?
                if (this.#record["confirmed_target_x"] === null) {
                    // Take the confirmed drop target from the auto target.
                    model["confirmed_target_x"] = this.#record["auto_target_x"];
                    model["confirmed_target_y"] = this.#record["auto_target_y"];
                }
            }

            json_object["crystal_well_droplocation_model"] = model;

            // Tell server to add response["html"] for next image in series.
            json_object[this.SHOULD_ADVANCE] = true;

            if (this.#crystal_well_index < this.#crystal_well_count - 1) {
                json_object[this.CRYSTAL_WELL_INDEX_NEXT] = this.#crystal_well_index + 1;
                json_object[this.CRYSTAL_WELL_COUNT] = this.#crystal_well_count;
            }

            // Send request to update database immediately.
            this.send(json_object);
        }

    } // end method

    // -------------------------------------------------------------
    // Handle previous or next button click.

    _handle_previous_or_next(direction) {
        var F = "echolocator__ImageEditUx::_handle_previous_or_next";

        // Request an update from the database.
        this.request_update(direction);

    } // end method

    // -------------------------------------------------------------
    // Handle where the user has moved the crosshairs, event comes from pixel_ux widget.
    // Units are transformed to underlying image pixel target.

    _handle_confirmed_target_ux_change_event(pixel_ux__user_change_event) {
        var F = "echolocator__ImageEditUx::_handle_confirmed_target_ux_change_event";

        var confirmed_target = pixel_ux__user_change_event.detail.target;

        // Mark image usable and save target location.
        this._send_update(true, confirmed_target)

    } // end method

    // -------------------------------------------------------------
    // Handle left click on the raphael paper.

    _handle_canvas_left_click(jquery_event_object) {
        var F = "echolocator__ImageEditUx::_handle_canvas_left_click";

        if (this.#record.is_exported_to_soakdb3) {
            console.log(F + ": ignoring canvas left click because is_exported_to_soakdb3 is " + this.#record.is_exported_to_soakdb3);
            return;
        }

        console.log(F + ": seeing canvas left click");

        var view_position = {
            x: jquery_event_object.offsetX,
            y: jquery_event_object.offsetY
        }

        // Convert to target position before giving to pixel_ux.
        var confirmed_target = this.#transformer.view_to_data(view_position);

        // Notify pixel_ux of requested change in position.
        this.#confirmed_target_ux.set_uuid(this.#crystal_well_index, confirmed_target);

        // Mark image usable and save target location.
        this._send_update(true, confirmed_target)

    } // end method

    // -------------------------------------------------------------
    // Handle right click on the raphael paper.

    _handle_canvas_right_click(jquery_event_object) {
        var F = "echolocator__ImageEditUx::_handle_canvas_right_click";

        if (this.#record.is_exported_to_soakdb3)
            return;

        // Mark image unusable.
        this._send_update(false)

    } // end method

    // -------------------------------------------------------------
    // Request update from database.

    request_update(direction) {
        var F = "echolocator__ImageEditUx::request_update";


        if (direction === null || direction === undefined)
            direction = 0;

        var new_crystal_well_index = this.#crystal_well_index;
        if (direction != 0) {
            new_crystal_well_index += direction;

            if (new_crystal_well_index >= this.#crystal_well_count)
                new_crystal_well_index = null;

            console.log(F + ": [CWINDX]" +
                " this.#crystal_well_index is " + this.#crystal_well_index +
                " moving to " + new_crystal_well_index +
                " in crystal_well_count " + this.#crystal_well_count);
        }

        // if (new_crystal_well_index < 0 || new_crystal_well_index >= this.#crystal_well_count) {
        //     return;
        // }


        var json_object = {}
        // TODO: Remove hardcoded "IMAGE_LIST_UX" in image edit's cookie list.
        json_object[this.ENABLE_COOKIES] = [this.COOKIE_NAME, "IMAGE_LIST_UX"]
        json_object[this.COMMAND] = this.FETCH_IMAGE;
        //json_object[this.SHOULD_ADVANCE] = true;
        json_object[this.CRYSTAL_WELL_INDEX] = new_crystal_well_index;

        this.send(json_object);

    } // end method

    // -------------------------------------------------------------
    // Handle an error response.

    handle_ajax_failure(response, status, jqXHR) {
        var F = "echolocator__ImageEditUx::handle_ajax_failure";

        // Let the base class check for and display any error or confirmation in the response.
        super.handle_ajax_failure(response, status, jqXHR);

        this.#jquery_objects.$hide_when_no_image.hide();

    } // end method

    // -------------------------------------------------------------
    // Handle the response when it comes.

    handle_ajax_success(response, status, jqXHR) {
        var F = "echolocator__ImageEditUx::_handle_ajax_success";

        // Let the base class check for and display any error or confirmation in the response.
        var error_message = super.handle_ajax_success(response, status, jqXHR);

        if (error_message !== null) {
            this.#jquery_objects.$hide_when_no_image.hide();
            return;
        }

        // Response is expected to contain the database record.
        var record = response.record;

        if (record === null) {
            if (response.confirmation === undefined) {
                console.log(F + ": response record had value of null");
                this.display_ajax_error("no image has been selected from the image list tab");
            }
            this.#jquery_objects.$hide_when_no_image.hide();
            return;
        }

        this.#jquery_objects.$hide_when_no_image.show();

        // Remember which set_crystal_well_index we are showing.
        this.#crystal_well_index = response[this.CRYSTAL_WELL_INDEX];
        this.#crystal_well_count = response[this.CRYSTAL_WELL_COUNT];

        // Display the index (plus 1 to be less confusing to viewer) and length.
        this.#jquery_objects.$crystal_well_index.text(this.#crystal_well_index + 1);
        this.#jquery_objects.$crystal_well_count.text(this.#crystal_well_count);

        this.#jquery_objects.previous_button.attr("disabled", this.#crystal_well_index == 0);
        this.#jquery_objects.next_button.attr("disabled", this.#crystal_well_index >= this.#crystal_well_count - 1);

        this.#jquery_objects.accept_button.attr("disabled", record.is_exported_to_soakdb3);
        this.#jquery_objects.reject_button.attr("disabled", record.is_exported_to_soakdb3);
        this.#jquery_objects.reset_button.attr("disabled", record.is_exported_to_soakdb3);

        this.#confirmed_target_ux.enabled(!record.is_exported_to_soakdb3)

        // Update the display with the new file's contents.
        var src = record.filename;
        this.#jquery_objects.$image.prop("src", src)

        // Render the set_crystal_well_index stuff.
        this.#jquery_objects.$filename.text(record.filename);

        if (record.number_of_crystals === null)
            record.number_of_crystals = "-";

        if (record.is_usable === null)
            record.is_usable = "undecided";
        if (record.is_usable === true)
            record.is_usable = "yes";
        if (record.is_usable === false)
            record.is_usable = "no";

        if (record.is_exported_to_soakdb3 === null)
            this.#jquery_objects.$is_exported_to_soakdb3.text("no");
        if (record.is_exported_to_soakdb3 === true)
            this.#jquery_objects.$is_exported_to_soakdb3.text("yes");
        if (record.is_exported_to_soakdb3 === false)
            this.#jquery_objects.$is_exported_to_soakdb3.text("no");

        this.#jquery_objects.$number_of_crystals.text(record.number_of_crystals);
        this.#jquery_objects.$is_usable.text(record.is_usable);

        // Keep the last record loaded.
        this.#record = record;

        // The the pixel ux about the set_crystal_well_index so it can be included in sending changes.
        var x = record.confirmed_target_x;
        if (x === null)
            x = record.auto_target_x;
        if (x === null)
            x = 10;

        var y = record.confirmed_target_y;
        if (y === null)
            y = record.auto_target_y;
        if (y === null)
            y = 10;

        var confirmed_target = { x: x, y: y };

        this.#confirmed_target_ux.set_uuid(this.#crystal_well_index, confirmed_target);

        // The the pixel ux about the set_crystal_well_index so it can be included in sending changes.
        var x = record.well_centroid_x;
        if (x === null)
            x = 100;

        var y = record.well_centroid_y;
        if (y === null)
            y = 100;

        var well_centroid = { x: x, y: y };
        var image_size = {
            w: record.width ? record.width : 100,
            h: record.height ? record.height : 100
        };

        this.#well_centroid_ux.set(well_centroid, image_size);

        // Let the spreader calculate the available space for the image.
        // This will trigger a call to this.handle_spread_event().
        // This only needs to be here for the very first opening of this tab.
        this.image1_spreader.spread();

        // Resize the image to fit on the screen.
        this.resize_image()
    } // end method 

    // -----------------------------------------------------------------------
    // Callback from the spreader event (window resize), after the image size is calculated.
    handle_spread_event(event) {
        var F = "echolocator__ImageEditUx::handle_spread_event";

        // Redraw after window size changed.
        this.render()

    } // end method

    // -----------------------------------------------------------------------
    // Called when window size changes.

    render() {
        var F = "echolocator__ImageEditUx::render";

        var w = $("#image1_viewport").width()
        var h = $("#image1_viewport").height()

        // console.log(F + " image1_viewport size is [" + w + ", " + h + "]");

        // Resize the annotation overlay.
        $("#raphael1_viewport").width(w)
        $("#raphael1_viewport").height(h)

        // To transform coordinates.
        this.#transformer.set_view({ x1: 0, y1: 0, x2: w, y2: h })

        // Resize the displayed image according to the current screen size.
        this.resize_image()

        // Tell pixel_ux to render under the new transformer.
        this.#confirmed_target_ux.render()
        this.#well_centroid_ux.render()

        this.$interaction_parent.focus();

    } // end method

    // -----------------------------------------------------------------------
    // Resize the displayed image according to the current screen size.

    resize_image() {
        var F = "echolocator__ImageEditUx::resize_image";

        if (this.#record === null)
            return;

        var record = this.#record;

        var w = record.width;
        var h = record.height;

        // console.log(F + " image data size is [" + w + ", " + h + "]");

        // To transform coordinates.
        this.#transformer.set_data({ x1: 0, y1: 0, x2: w, y2: h })

        // Transform data to view.
        var view_position = this.#transformer.data_to_view({ x: w, y: h })

        // console.log(F + " data to view is [" + view_position.x + ", " + view_position.y + "]");

        // TODO: Move detector1_image resize into image_edit_ux.
        var $img = $("#detector1_image")
        $img.prop("width", view_position.x)
        $img.prop("height", view_position.y)

    } // end method

} // end class