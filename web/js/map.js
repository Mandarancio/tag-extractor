//Fichier javascript pour la géolocalisation
function initialize() {

	var latitude = 46.2;
	var longitude = 6.15;

	var latlng01 = new google.maps.LatLng(latitude, longitude);

	var options = {
			center: latlng01,
			zoom: 14,
			//mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById("map_geolocalisation"), options);

	$.ajax({
		url: "http://localhost/RC/DB/model/get_pict.php",
		dataType: 'json',
		success: function(json1) {
			$.each(json1, function(key, data) {
			var position = new google.maps.LatLng(data.lat, data.lng); 
			var info_content='<div class="info_content">';
			$.each(data.pict, function(pict_key, pict_data) {
				info_content = info_content+
							   '<div class="info">'+
								   '<h3>'+pict_data.categorie+'</h3>' +
								   '<p>'+pict_data.tag+'</p>' +
								   '<p><strong>L\'image est-elle bien classifiée?</strong> </p>'+
									'<input type="radio" name="validate" value="1"> Oui'+
									'<input style="margin-left:10px; " type="radio" name="validate" value="0">Non'+
							   '</div>'+
							   '<div class="image_content">' +
									'<img src="'+pict_data.url+'" alt="image inaccessible">'+
							   '</div>';
			});
			info_content = info_content+'</div>';
			//Creating a marker and putting it on the map
			create_marker(map, position, info_content);
		});

		},
		error: function(xhr, status, error) {
			var acc = []
			$.each(xhr, function(index, value) {
				acc.push(index + ': ' + value);
			});
			alert(JSON.stringify(acc));
		}
	}); 
}
// event when radio button is checked
// $(document).ready(function() {
			// $('input[name=validate]').on('change', function() {
				// var option=$(this).val();
				// $.ajax({
				// type: "POST",
				// url: "http://localhost/RC/DB/model/validate.php",
				// data: {}, // send data: id_categ ; id_pict ; value_of_the_radio_button
				// success:function() {
					// alert('ok');
				// },
				// error: function(xhr, status, error) {
					// var acc = []
					// $.each(xhr, function(index, value) {
						// acc.push(index + ': ' + value);
					// });
					// alert(JSON.stringify(acc));
				// }
			// });
			// });	
		// });

function create_marker(map, latlng, info_content){
	var marker = new google.maps.Marker({
		position: latlng,
		map: map,
		title: "Marker"
	});

	var content = info_content;

	var infowindow = new google.maps.InfoWindow({
		content: content
	});

	marker.addListener('click', function() {
		infowindow.open(map, marker);
	});

}

google.maps.event.addDomListener(window, 'load', initialize);


