
function initialize() {
  
    var locallatlng = new google.maps.LatLng(42.375492,-71.116948);
    var worldlatlng = new google.maps.LatLng(25,0);

    var mapOptions = {
        zoom: 1,
        center: worldlatlng
    }

    var mapOptionsLocal = {
        zoom: 7,
        center: locallatlng
    }

    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    var maplocal = new google.maps.Map(document.getElementById('maplocal'), mapOptionsLocal);

    var url = jQuery('#data_url').text();

    jQuery.get(url, {}, function(data) {
    
        jQuery(data).find("marker").each(function() {
            var marker = jQuery(this);
            var latlng = new google.maps.LatLng(parseFloat(marker.attr("lat")), parseFloat(marker.attr("lng")));
            var content = marker.find("content").html();
            var markerlocal = new google.maps.Marker({position: latlng, map: maplocal});
            var marker = new google.maps.Marker({position: latlng, map: map});

            var infowindow = new google.maps.InfoWindow({
                content: content
            });

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(map,marker);
            });

            google.maps.event.addListener(markerlocal, 'click', function() {
                infowindow.open(maplocal,markerlocal);
            });
        });
    });
}

google.maps.event.addDomListener(window, 'load', initialize);
