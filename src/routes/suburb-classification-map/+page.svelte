<script>
	import { onMount } from 'svelte';
	import mapboxgl from "mapbox-gl";
    import cmaSummary from './data/cma-summary.json';
    import Select from 'svelte-select';
	import '../../assets/global-styles.css';

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
	let cmaSelected = 'Toronto';
    let selectedPop = '-';
    let selectedActive = '-';
    let selectedTransit = '-';
    let selectedAuto = '-';
    let selectedExurban = '-';

   // $: console.log(cmaPopulation);

    // create map variable to fill in with onMount
    let map;
    let selectedCtuid = '';
    let selectedClass = '';
    let selectedCtPop = ''
    let selectedPercActive =''
    let selectedPercTransit =''
    let selectedPercAuto = ''
    let ctuid = '0';


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
        selectedPop = (filteredData.pop2021);
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
            "suburbs-project-cma", 
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
            minZoom: 5,
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

        map.on('click' , 'suburbs-project-ct' , (e) => {
            selectedCtuid = e.features[0].properties.ctuid;
            selectedClass = e.features[0].properties.class;
            selectedCtPop = (e.features[0].properties.pop2021);
            selectedPercActive = ((e.features[0].properties.active)*100).toFixed(1);
            selectedPercTransit = ((e.features[0].properties.transit)*100).toFixed(1);
            selectedPercAuto = ((e.features[0].properties.auto)*100).toFixed(1);

        })

        map.on('click', 'suburbs-project-ct', (e) => {		

			var features = map.queryRenderedFeatures(e.point, { layers: ['suburbs-project-ct'] });

			if (ctuid != features[0].properties.ctuid) {
				var style = [
					"match",
					["get", "ctuid"],
					[features[0].properties.ctuid],
					"#6D247A",
					"#fff",
				]
				map.setPaintProperty('suburbs-project-ct', 'fill-outline-color', style)
				ctuid = features[0].properties.ctuid
			} 
		});

        map.setPaintProperty ('suburbs-project-cma' , 'fill-color' , 'red');

    });

    let isChecked = false;
 
  function toggleCheckbox() {
 	isChecked = !isChecked;
 	if (isChecked) {
        map.setPaintProperty('suburbs-project-ct', 'fill-opacity', 0.42);
        map.setPaintProperty('mapbox-satellite', 'raster-opacity', 1.00);
 	} 
    else {
        map.setPaintProperty('suburbs-project-ct', 'fill-opacity', 0.7);
        map.setPaintProperty('mapbox-satellite', 'raster-opacity', 0);
    }
    };

function reset() {
    cmaX = '';
    cmaY = '';
    cmaSelected = '';
}
 
  
</script>


<svelte:head>
	<link href='https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.css' rel='stylesheet' />
</svelte:head>


<main>

        

    <div id="content">

        <h1>Canadian Suburbs Atlas</h1>

        <div class="bar"></div>

        <p>
            This map visualizes how suburbanized Canadian cities are. Read about the methods <a href="https://www.canadiansuburbs.ca/research-papers/">here</a>. Select below to view a map and stats for a specific Census Metropolitan Area (CMA).
        </p>

        <div class="bar"></div>

        <Select 
            items={cmaAll} 
            value={cmaSelected} 
            clearable={false} 
            showChevron={true} 
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

        <div class="bar"></div>

        <div id="legend-wrapper">
            <svg id="legend"  width="300" height="130">
                
                <text x="10" y="20" class="legend-text" font-size="12" fill="black">Population (2021): {selectedPop.toLocaleString()}</text>

                <rect class="legend-bar" x="30" y="30" width="{200 * selectedActive / 100}" height="15"/>
                <rect class="legend-box" x="10" y="30" width="15" height="15" fill="#8DBF2E" />
                <text x="30" y="42" class="legend-text" font-size="12" fill="black">Active Core: <tspan font-weight="bold">{selectedActive}%</tspan> ({Math.round(selectedPop * selectedActive / 100).toLocaleString()} people)</text>

                <rect class="legend-bar" x="30" y="50" width="{200 * selectedTransit / 100}" height="15"/>
                <rect class="legend-box" x="10" y="50" width="15" height="15" fill="#00A189" />
                <text x="30" y="62" class="legend-text" font-size="12" fill="black">Transit Suburb: <tspan font-weight="bold">{selectedTransit}%</tspan> ({Math.round(selectedPop * selectedTransit / 100).toLocaleString()} people)</text>

                <rect class="legend-bar" x="30" y="70" width="{250 * selectedAuto / 100}" height="15"/>
                <rect class="legend-box" x="10" y="70" width="15" height="15" fill="#F1C500" />
                <text x="30" y="82" class="legend-text" font-size="12" fill="black">Auto Suburb: <tspan font-weight="bold">{selectedAuto}%</tspan> ({Math.round(selectedPop * selectedAuto / 100).toLocaleString()} people)</text>

                <rect class="legend-bar" x="30" y="90" width="{200 * selectedExurban / 100}" height="15"/>
                <rect class="legend-box" x="10" y="90" width="15" height="15" fill="#f7f2df" />
                <text x="30" y="102" class="legend-text" font-size="12" fill="black">Exurb: <tspan font-weight="bold">{selectedExurban}%</tspan> ({Math.round(selectedPop * selectedExurban / 100).toLocaleString()} people)</text>

                <rect class="legend-box" x="10" y="110" width="15" height="15" fill="#D0D1C9" />
                <text x="30" y="122" class="legend-text" font-size="12" fill="black">Unclassified / No Data: 0%</text>

            </svg>
        </div>

        <div class="bar"></div>



        <label>
            <input type="checkbox" on:change={toggleCheckbox}>Satellite View
        </label>



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

       <p>
            This map was built by QQQ and QQQ at the School of Cities. The code for this map is on GitHub
        </p>
    </div>

    
    
   <!-- <div id="slider">
        
        Satellite
        <label class="switch">
            <input type="checkbox">
            <span class="slider round"></span>
          </label>

    </div>-->

    <!-- <div id = 'reset'>
        <button on:click = {reset}> reset</button>
    </div> -->

	<div id="map"></div>

</main>


<style>

	:global(body) {
		padding: 0px;
		margin: 0px;
		background-color: var(--brandDarkBlue);
	}
	
	
    main {
		margin: auto 0px;
        padding: 0px;
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
        min-width: 350px;
		position: absolute;
		z-index: -99;
	}

    h1 {
        font-size: 27px;
        font-family: TradeGothicBold;
        margin: 0px;
        padding: 10px;
        padding-bottom: 5px;
        color: var(--brandDarkBlue);
    }

    p {
        font-size: 15px;
        font-family: TradeGothicBold;
        margin: 0px;
        padding: 0px;
        padding-left: 10px;
        padding-right: 10px;
        padding-bottom: 5px;
        padding-top: 5px;
        color: var(--brandGray70);
    }

    a {
        color: var(--brandMedBlue);
    }

    #content {
        width: 300px;
        height: 460px;
        position: absolute;
        top: 5px;
        left: 5px;
        background-color: white; 
        border: solid 1px lightgrey;
        border-radius: 5px;
        z-index: 1; 
    }

    .bar {
        height: 1px;
        width: 290px;
        background-color: var(--brandDarkBlue);
        padding: 0px;
        margin: 0px;
        margin-left: 5px;
        opacity: 0.25;
    }

    #legend {
        background-color: white;
    }

    .legend-box {
        stroke: white;
        stroke-width: 0.5px;
    }

    .legend-bar {
        fill: #efefef;
        stroke: #cecece;
        stroke-width: 0.5px;
    }

    #box {
        position: absolute;
        font: 14px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
        background: #2b1102;
        color: rgb(231, 226, 226);
        width: 260px;
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
