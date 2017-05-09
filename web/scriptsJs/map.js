//Fichier javascript pour la géolocalisation

function initialize() {

	var latitude = 46.2;
	var longitude = 6.15;

	var latlng = new google.maps.LatLng(latitude, longitude);

	var options = {
			center: latlng,
			zoom: 15,
			mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById("map_geolocalisation"), options);


	//On vérifie que l'utilisateur possède la géocalisation ou non
	/*if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(successCallback, null, {enableHighAccuracy:true});
	}
	else{
	  //alert("Votre navigateur ne supporte pas le système de géolocalisation");
	}*/

}

//Si la géocalisation fonctionne, on change la latitude et la longitude par rapport aux nouvelles coordonnées
function successCallback(position){
	//panTo permet de centrer notre carte sur nos nouvelles coordonnées
	map.panTo(new google.maps.LatLng(position.coords.latitude, position.coords.longitude));
	/*var marker = new google.maps.Marker({
		position: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),
		map: map
	});*/

}

google.maps.event.addDomListener(window, 'load', initialize);
