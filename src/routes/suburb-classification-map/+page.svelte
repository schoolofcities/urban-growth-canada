<script>
	import { onMount } from 'svelte'
	import mapboxgl from "mapbox-gl";
    import cmaSummary from './data/cma-summary.json';
    import Typeahead from "svelte-typeahead";
    import Select from 'svelte-select';
	import '../../assets/global-styles.css';

	mapboxgl.accessToken = 'pk.eyJ1Ijoic2Nob29sb2ZjaXRpZXMiLCJhIjoiY2w2Z2xhOXprMTYzczNlcHNjMnNvdGlmNCJ9.lOgVHrajc1L-LlU0as2i2A';

    // array of all cma names
    let cmaAll = cmaSummary
        .sort((a, b) => b.pop2021 - a.pop2021)
        .map(item => item.cmaname);
        
    // initial cma selected
	let cmaSelected = 'Montreal';
    $: console.log(cmaSelected);

    // create map variable to fill in with onMount
    let map;

    // function for what to do when new cma is selected
    function handleSelect(e) {

        // reset cma selected variable
        cmaSelected = e.detail.value;

        // filter cma data to just the cma we selected
        let filteredData = cmaSummary.filter(item => item.cmaname === cmaSelected)[0];

        // pan and zoom to the new cma
        map.setZoom(10);
        map.panTo([filteredData.x, filteredData.y]);

        // filter the base map data

    }










    // const name = raw.map(cityname => cityname.cmaname);
    // const cords = raw.map(citycord => ({ x: citycord.x , y: citycord.y}));

    onMount(() => {
        map = new mapboxgl.Map({
            container: 'map', 
            style: 'mapbox://styles/schoolofcities/cli0otj3n04m601pa9s0s0mc4',
            center: [-73.628, 45.575], 
            zoom: 10,
            maxZoom: 14,
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

    <div id="select">
        <Select 
            items={cmaAll} 
            value={cmaSelected} 
            clearable={false} 
            showChevron=true 
            on:input={handleSelect}
            --background="white"
            --height="20px"
            --item-color="black"
            --border-radius="0"
            --border="1px"
            --list-border-radius="0px"
            --font-size="15px"
            --max-height="30px"
            --item-is-active-color="black"
            --item-is-active-bg="lightgrey"

        />
    </div>
      
	<div id="map"></div>

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

    #select {
        width: 250px;
        height: 30px;
        position: absolute;
        top: 5px;
        left: 5px;
        background-color: white; 
        border: solid 1px var(--brandDarkBlue);
        z-index: 1; 
    }

    #select p {
        font-size: 12px;
        margin: 0px;
        padding: 0px;
        padding-left: 20px;
    }
	
</style>
