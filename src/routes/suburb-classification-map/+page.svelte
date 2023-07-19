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

        let cmaX = filteredData.x;
        let cmaY = filteredData.y;
        let cmauid = filteredData.cmauid.toString();

        // pan and zoom to the new cma - reset pitch and bearing if they changed
        map.setZoom(9);
        map.setBearing(0);
        map.setPitch(0);
        map.panTo([cmaX, cmaY]);

        // filter the base map data
        map.setFilter(
            "suburbs-project-ct", 
            [
                "match",
                ["get", "cmaname"],
                [cmaSelected],
                true,
                false
            ]
        );
        map.setFilter(
            "suburbs-project-cma", 
            [
                "match",
                ["get", "CMAUID"],
                [cmauid],
                true,
                false
            ]
        );
    }

    onMount(() => {
        map = new mapboxgl.Map({
            container: 'map', 
            style: 'mapbox://styles/schoolofcities/cli0otj3n04m601pa9s0s0mc4',
            center: [-73.628, 45.575], 
            zoom: 9,
            maxZoom: 14,
            minZoom: 1,
            scrollZoom: true,
            attributionControl: false
        });

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
