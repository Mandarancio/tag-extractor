//Fichier javascript pour la géolocalisation

function initialize() {

	var latitude = 46.2;
	var longitude = 6.15;

	var latlng = new google.maps.LatLng(latitude, longitude);

	var options = {
			center: latlng,
			zoom: 15,
			//mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById("map_geolocalisation"), options);

	create_marker(map, latlng);

}

function create_marker(map, latlng){
	var marker = new google.maps.Marker({
		position: latlng,
		map: map,
		title: 'My marker'
	});

	var contentString = 'test';

	var infowindow = new google.maps.InfoWindow({
		content: contentString
	});

	var marker = new google.maps.Marker({
		position: latlng,
		map: map,
		title: 'AYAHHHHHH'
	});
	marker.addListener('click', function() {
		infowindow.open(map, marker);
	});

}

google.maps.event.addDomListener(window, 'load', initialize);
