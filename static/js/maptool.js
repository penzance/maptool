$(document).ready(function(){

    $('.deleteRow').click(function(e){
        var id = $(this).attr('data-id');
        var thisrow =  $(this);
        var url = "/lti_tools/maptoolapp/deleteview";
        if (confirm('Are you sure you want to delete the view?')) {
            var formData = {
                'id' : id
            };
            $.ajax({
                url : url ,
                type : "POST",
                data : formData,
                success : function(json) {
                        thisrow.remove();
                },
            });
            e.preventDefault();
        }
    });

    $('.selectView').click(function(e){
        $(this).closest("form").submit();
    });

    function initialize() {

        var map;

        // get a list of all the map divs that contain map data
        maplist = $(".map-style");

        // for each div, create the map from the data attributes
        $.each(maplist, function(){

            lat = $(this).attr("data-lat");
            long = $(this).attr("data-long");
            item_group_id = $(this).attr("data-item-group-id");
            id = $(this).attr("id");

            zoom = parseInt($(this).attr("data-zoom"));
            if(isNaN(zoom)){
                // set the default zoom to 8 if none can be determined
                zoom = 8;
            }

            var mapOptions = {
                zoom: zoom,
                center: new google.maps.LatLng(lat, long)
            };

            map = new google.maps.Map(document.getElementById(id), mapOptions);

// this part is a work in progress
// 				  	url = "http://cscie12students.dce.harvard.edu/~eparker/test/"+item_group_id + ".xml";
//
// 					$.ajax({
// 						url: url,
// 						method: 'GET',
// 						dataType: 'xml'
// 						}).done(function(data){
// 							console.log("hello");
// 							jQuery(data).find("marker").each(function() {
// 								var marker = jQuery(this);
// 								var latlng = new google.maps.LatLng(parseFloat(marker.attr("lat")), parseFloat(marker.attr("lng")));
// 								var content = marker.find("content").html();
// 								console.log(content);
// 								var marker = new google.maps.Marker({position: latlng, map: map});
//
//
// 								var infowindow = new google.maps.InfoWindow({
// 									content: content
// 								});
//
// 								google.maps.event.addListener(marker, 'click', function() {
// 									infowindow.open(map,marker);
// 								});
// 							});
// 						}).fail(function(){
//         					console.log("Failure args: ", arguments);
//     					});

        });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
});