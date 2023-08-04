<script>
	import { onMount } from 'svelte'
	import mapboxgl from "mapbox-gl";
    import cmaSummary from './suburb-classification-map/data/cma-summary.json';
    import Typeahead from "svelte-typeahead";
    import Select from 'svelte-select';
	//import '../../assets/global-styles.css';

	mapboxgl.accessToken = 'pk.eyJ1Ijoic2Nob29sb2ZjaXRpZXMiLCJhIjoiY2w2Z2xhOXprMTYzczNlcHNjMnNvdGlmNCJ9.lOgVHrajc1L-LlU0as2i2A';

    // array of all cma names
    let cmaAll = cmaSummary
        .sort((a, b) => b.pop2021 - a.pop2021)
        .map(item => item.cmaname);
        
    // array of populations
    let cmaPopulation = cmaSummary
        .sort((a, b) => b.pop2021 - a.pop2021)
        .map(item => item.pop2021);
    
        
    // initial cma selected
	let cmaSelected = '';
    let selectedPop = '-';
    let selectedActive = '-';
    let selectedTransit = '-';
    let selectedAuto = '-';
    let selectedExurban = '-';

    $: console.log(cmaPopulation);

    // create map variable to fill in with onMount
    let map;
    let selectedCtuid = '';
    let selectedClass = '';
    let selectedCtPop = ''
    let selectedPercActive =''
    let selectedPercTransit =''
    let selectedPercAuto = ''


    // function for what to do when new cma is selected
    function handleSelect(e) {

        // reset cma selected variable
        cmaSelected = e.detail.value;

        // filter cma data to just the cma we selected
        let filteredData = cmaSummary.filter(item => item.cmaname === cmaSelected)[0];

        let cmaX = filteredData.x;
        let cmaY = filteredData.y;
        let cmauid = filteredData.cmauid.toString();
        
        //change data values based on cma selected
        selectedPop = (filteredData.pop2021).toLocaleString();
        selectedActive = ((filteredData.active) * 100).toFixed(1);
        selectedTransit = ((filteredData.transit) * 100).toFixed(1);
        selectedAuto = ((filteredData.auto) * 100).toFixed(1);
        selectedExurban = ((filteredData.exurban) * 100).toFixed(1);

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
                .setHTML("CTUID: " + e.features[0].properties.ctuid + "Class:"+ e.features[0].properties.class) //indexes the GeoJSON code for the CTUID from properties
                .addTo(map);
        });

       /* map.on('click', 'suburbs-project-ct', (e) => {		
			map.setPaintProperty('suburbs-project-ct' , 'fill-color' , 'pink')
        });*/

        map.on('click' , 'suburbs-project-ct' , (e) => {
            selectedCtuid = e.features[0].properties.ctuid;
            selectedClass = e.features[0].properties.class;
            selectedCtPop = (e.features[0].properties.pop2021);
            selectedPercActive = ((e.features[0].properties.active)*100).toFixed(1);
            selectedPercTransit = ((e.features[0].properties.transit)*100).toFixed(1);
            selectedPercAuto = ((e.features[0].properties.auto)*100).toFixed(1);

        })

        map.on('click' , 'suburbs-project-ct' , () => {
            map.setPaintProperty('suburbs-project-cma' , 'fill-color' , 'red');
        }
        );
    });

    let isChecked = false;
 
  function toggleCheckbox() {
 	isChecked = !isChecked;
 	if (isChecked) {
    map.setPaintProperty('suburbs-project-ct', 'fill-opacity', 0.50);
    map.setPaintProperty('mapbox-satellite', 'raster-opacity', 1.00);
 	} 
    else {
    map.setPaintProperty('suburbs-project-ct', 'fill-opacity', 0.68);
    map.setPaintProperty('mapbox-satellite', 'raster-opacity', 0.00); 	
    }

  };

function reset() {
    console.log('it worked');
}
 
  
</script>


<svelte:head>
	<link href='https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.css' rel='stylesheet' />
</svelte:head>


<main>

<div id= "test">    
    <label>
        <input type="checkbox" on:change={toggleCheckbox}>
    </label>
</div>

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
        <div id="data">
        Population: {selectedPop}
        <br>Active: {selectedActive}%
        <br>Transit:{selectedTransit}%
        <br>Auto: {selectedAuto}%
        <br>Exurban: {selectedExurban}%
    </div>
    </div>

    <div id="box">
         CTUID: {selectedCtuid}
         <br>Classification: {selectedClass}
         <br>Total Population: {selectedCtPop}
         <br>
         <br>Mode Share
         <br>Active: {selectedPercActive}%  
         Transit:{selectedPercTransit}%  
         Auto:{selectedPercAuto}%  
        </div>
    
   <!-- <div id="slider">
        
        Satellite
        <label class="switch">
            <input type="checkbox">
            <span class="slider round"></span>
          </label>

    </div>-->

<div id = 'reset'>
    <button on:click = {reset}> reset</button>
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

    #test {
        position: relative;
        top: 700px;
        left: 1160px;
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

    #data {
        display: flex;
        font-size: large;
        width: 250px;
        background-color: aqua;
        justify-content: center;
        align-items: center;
        border: 2px solid black;
        
    }
    
    #select p {
        font-size: 12px;
        margin: 0px;
        padding: 0px;
        padding-left: 20px;
    }

    #box {
    position: absolute;
    font: 14px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
    background: #2b1102;
    color: rgb(231, 226, 226);
    width: 260px;
    top: 570px;
    left: 1200px;
    margin-top: 10px;
    padding: 10px;
    overflow: visible;
    opacity: 1;
}

    #reset {
        position: absolute;
        top: 15px;
        left: 260px;
    }

  /*  #slider {
        position: relative;
        width: 60px;
        height: 34px;
        top: 650px;
        left: 1140px;

    }

    .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

    .switch input { 
    opacity: 0;
    width: 0;
    height: 0;
}

    .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
}

    .slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
}

    input:checked + .slider {
  background-color: #2196F3;
}

    input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
}

    input:checked + .slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
}
*/
/* Rounded sliders */
    .slider.round {
    border-radius: 34px;
}

    .slider.round:before {
    border-radius: 50%;
}
	
</style>
