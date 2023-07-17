<script>
	import { onMount } from 'svelte'
	import mapboxgl from "mapbox-gl";
    import raw from 'C:/Users/Remus/Desktop/School/Work Study/3-Website/urban-growth-canada/src/routes/suburb-classification-map/data/cma-summary.json'
    //import Typeahead from 'svelte-typeahead/types/Typeahead.svelte';
	//import '../../assets/global-styles.css';

	mapboxgl.accessToken = 'pk.eyJ1Ijoic2Nob29sb2ZjaXRpZXMiLCJhIjoiY2w2Z2xhOXprMTYzczNlcHNjMnNvdGlmNCJ9.lOgVHrajc1L-LlU0as2i2A';

	// global cma variable
	let cma = 'Toronto';
    let map;

    const name = raw.map(cityname => cityname.cmaname);
    const cords = raw.map(citycord => ({ x: citycord.x , y: citycord.y}));

console.log(cords)
console.log(name)

//Map and its elements
	onMount(() => {
		map = new mapboxgl.Map({
			container: 'map', 
			style: 'mapbox://styles/schoolofcities/cli0otj3n04m601pa9s0s0mc4',
			center: [-73.628, 45.575], 
			zoom: 10,
			maxZoom: 11,
			minZoom: 1,
			scrollZoom: true,
			attributionControl: false
		});
	// Knick knacks	
	map.addControl(new mapboxgl.NavigationControl(), 'top-right');

		const scale = new mapboxgl.ScaleControl({
			maxWidth: 100,
			unit: 'metric'
			});

	map.addControl(scale, 'bottom-right');


    // Mouse functions
    map.on('mouseenter', 'suburbs-project-ct', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'suburbs-project-ct', () => {
        map.getCanvas().style.cursor = '';
    });

    map.on('click', 'suburbs-project-ct', (e) => {
        new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML("CMA: " + e.features[0].properties.cmaname) //indexes the GeoJSON code for the CTUID from properties
            .addTo(map);
    });


/*  
map.on('click', 'suburbs-project-ct', (e) => {		

    var features = map.queryRenderedFeatures(e.point, { layers: ['suburbs-project-ct'] });

    if (ctuid != features[0].properties.ctuid) {
        var style = [
            "match",
            ["get", "CTUID"],
            [features[0].properties.ctuid],
            "#f1c500",
            "#fff"
        ]
        map.setPaintProperty('suburbs-project-ct', 'fill-color', style)
        ctuid = features[0].properties.ctuid
        } 
    else {
    map.setPaintProperty('suburbs-project-ct', 'fill-color', '#fff')
    ctuid = '0'
    }

});

function placeClick(city) {
		cmaname = "0";
		map.setPaintProperty('ct_fill', 'fill-color', '#fff');
		map.panTo(city.original.geometry.coordinates);
		map.zoonTo(10);
	}
*/

});

</script>


<svelte:head>
	<link href='https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.css' rel='stylesheet' />
</svelte:head>


<main>

	<div id="map"></div>

<!--
    <div id="search">
        <Typeahead
                {data}
                label=""
                inputAfterSelect="clear"
                placeholder={`search and zoom to a cma`}
                limit={5}
                extract={(item) => item.properties.cmaname}
                on:select={({ detail }) => placeClick(detail)}
                let:result
            >
            <span id="search-results">{@html result.string}</span>
        </Typeahead>
    
    </div>
-->
</main>


<style>

	:global(body) {
		padding: 0px;
		margin: 0px;
		background-color: var(--brandDarkBlue);
	}
	
	main {
		margin: auto;
		width: 100%;
		height: 100%;
	}

	#map {
		height: 100%;
		width: 100%;
		position: absolute;
		z-index: -99;
	}
	
</style>
