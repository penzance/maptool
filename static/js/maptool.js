$(document).ready(function() {

    // Allows an instructor to delete a view from the tool
    $('.deleteRow').click(function(e) {
        var id = $(this).attr('data-id');
        var thisrow = $(this);
        var url = "/lti_tools/maptoolapp/deleteview";
        if (confirm('Are you sure you want to delete the view?')) {
            var formData = {
                'id': id,
                'class': 'deleteRow'
            };
            $.ajax({
                url: url,
                type: "POST",
                data: formData,
                success: function(json) {
                    thisrow.remove();
                },
            });
            e.preventDefault();
        }
    });

    // Allows a student to delete the points that they added to the class map
    $('.delete-point').click(function(e) {
        var id = $(this).attr('data-id');
        var thisrow = $(this);
        var url = "/lti_tools/maptoolapp/deleteview";
        if (confirm('Are you sure you want to delete this point?')) {
            var formData = {
                'id': id,
                'class': 'delete-point'
            };
            $.ajax({
                url: url,
                type: "POST",
                data: formData,
                success: function(json) {
                    thisrow.remove();
                    initialize();
                }
            });
        }
    });

    $('.selectView').click(function(e) {
        $(this).closest("form").submit();
    });

    // Initialize maps on map_view.html
    function initialize() {
        var map_1 = document.querySelector('#map_canvas_1');
        var map_2 = document.querySelector('#map_canvas_2');
        var map_3 = document.querySelector('#map_canvas_3');
        item_group_id = map_1.dataset.item_group_id;
        lat_1 = map_1.dataset.lat;
        long_1 = map_1.dataset.long;
        zoom_1 = parseInt(map_1.dataset.zoom);
        var mapOptions_1 = {
            zoom: zoom_1,
            center: new google.maps.LatLng(lat_1, long_1)
        };
        var map_canvas_1 = new google.maps.Map(document.getElementById('map_canvas_1'), mapOptions_1);

        if (map_2 != null) {
            console.log('made it');
            lat_2 = map_2.dataset.lat;
            long_2 = map_2.dataset.long;
            zoom_2 = parseInt(map_2.dataset.zoom);
            var mapOptions_2 = {
                zoom: zoom_2,
                center: new google.maps.LatLng(lat_2, long_2)
            };
            var map_canvas_2 = new google.maps.Map(document.getElementById('map_canvas_2'), mapOptions_2);
        }
        if (map_3 != null){
            lat_3 = map_3.dataset.lat;
            long_3 = map_3.dataset.long;
            zoom_3 = parseInt(map_3.dataset.zoom);
            var mapOptions_3 = {
                zoom: zoom_3,
                center: new google.maps.LatLng(lat_3, long_3)
            };
            var map_canvas_3 = new google.maps.Map(document.getElementById('map_canvas_3'), mapOptions_3);
        }

        // get a list of all the map divs that contain map data
        var url = jQuery('#data_url').text();
        jQuery.get(url, {}, function(data) {
            jQuery(data).find("marker").each(function() {
                var marker = jQuery(this);
                var latlng = new google.maps.LatLng(parseFloat(marker.attr(
                    "lat")), parseFloat(marker.attr("lng")));
                var content = marker.find("content").html();
                var marker_1 = new google.maps.Marker({
                    position: latlng,
                    map: map_canvas_1
                });
                var infowindow = new google.maps.InfoWindow({
                    content: content
                });
                google.maps.event.addListener(marker_1, 'click',
                    function() {
                        infowindow.open(map_canvas_1, marker_1);
                    });
                if (map_2 != null) {
                    var marker_2 = new google.maps.Marker({
                        position: latlng,
                        map: map_canvas_2
                    });
                    google.maps.event.addListener(marker_2, 'click',
                        function() {
                            infowindow.open(map_canvas_2, marker_2);
                    });
                }
                if (map_3 != null) {
                    var marker_3 = new google.maps.Marker({
                        position: latlng,
                        map: map_canvas_3
                    });
                    google.maps.event.addListener(marker_3, 'click',
                        function() {
                            infowindow.open(map_canvas_3, marker_3);
                    });
                }
            });
        });
    }
    google.maps.event.addDomListener(window, 'load', initialize);
});