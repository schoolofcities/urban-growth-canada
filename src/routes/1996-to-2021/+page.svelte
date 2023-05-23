<script>
	import { onMount } from 'svelte'
	import mapboxgl from "mapbox-gl";
	import Typeahead from "svelte-typeahead";
	import Places from "./assets/places.geo.json";
	import Info from "./lib/Info.svelte";
	import Select from "./lib/Select.svelte";
	import Header from "../../lib/Header.svelte";

	mapboxgl.accessToken = 'pk.eyJ1Ijoic2Nob29sb2ZjaXRpZXMiLCJhIjoiY2w3aml0dHdlMHlpazNwbWh0em4xOHNlaCJ9.fXNtPGq0DqYiFvPH6p4fjQ';

	const data = Places.features;

	let map;
	let ctuid = "0";

	let pageWidth;

	let metric = '';

	const hash = window.location.hash.substring(1);
	if (hash === 'population') {
		window.location.hash = 'population';
		metric = 'population';
	} else if (hash === 'dwellings') {
		window.location.hash = 'dwellings';
		metric = 'dwellings';
	} else {
		window.location.hash = 'population';
		metric = 'population';
	}
	

	function setMetric(value) {
		
		if (map) {
			metric = value;

			if (metric === 'population') {
				window.location.hash = 'population';
				map.setPaintProperty('pop_growth', 'circle-opacity', 0.8);
				map.setPaintProperty('pop_decline', 'circle-opacity', 0.8);
				map.setPaintProperty('pop_growth', 'circle-stroke-opacity', 1);
				map.setPaintProperty('pop_decline', 'circle-stroke-opacity', 1);
				map.setPaintProperty('dwe_growth', 'circle-opacity', 0);
				map.setPaintProperty('dwe_decline', 'circle-opacity', 0);
				map.setPaintProperty('dwe_growth', 'circle-stroke-opacity', 0);
				map.setPaintProperty('dwe_decline', 'circle-stroke-opacity', 0);
			} 
			else {
				window.location.hash = 'dwellings';
				map.setPaintProperty('pop_growth', 'circle-opacity', 0);
				map.setPaintProperty('pop_decline', 'circle-opacity', 0);
				map.setPaintProperty('pop_growth', 'circle-stroke-opacity', 0);
				map.setPaintProperty('pop_decline', 'circle-stroke-opacity', 0);
				map.setPaintProperty('dwe_growth', 'circle-opacity', 0.8);
				map.setPaintProperty('dwe_decline', 'circle-opacity', 0.8);
				map.setPaintProperty('dwe_growth', 'circle-stroke-opacity', 1);
				map.setPaintProperty('dwe_decline', 'circle-stroke-opacity', 1);
			}
		}
		
	}

	
	
	
	onMount(() => {
		map = new mapboxgl.Map({
			container: 'map', 
			style: 'mapbox://styles/schoolofcities/cl7j75gbd003b14ocub8skc7c',
			center: [-79.45, 43.65], 
			zoom: 10,
			maxZoom: 12,
			minZoom: 5,
			projection: 'globe',
			scrollZoom: true,
			attributionControl: false
		});
		
		
		map.addControl(new mapboxgl.AttributionControl({
			customAttribution: 'Map by <a href="http://jamaps.github.io/about.html">Jeff Allen</a>'
		}), 'bottom-right');
		map.addControl(new mapboxgl.NavigationControl(), 'top-right');

		const scale = new mapboxgl.ScaleControl({
			maxWidth: 100,
			unit: 'metric'
			});
		map.addControl(scale, 'bottom-right');

		map.on('mouseenter', 'ct_fill', () => {
			map.getCanvas().style.cursor = 'pointer';
		});
		map.on('mouseleave', 'ct_fill', () => {
			map.getCanvas().style.cursor = '';
		})

		map.on('click', 'ct_fill', (e) => {		

			var features = map.queryRenderedFeatures(e.point, { layers: ['ct_fill'] });

			if (ctuid != features[0].properties.CTUID) {
				var style = [
					"match",
					["get", "CTUID"],
					[features[0].properties.CTUID],
					"#f1c500",
					"#fff"
				]
				map.setPaintProperty('ct_fill', 'fill-color', style)
				ctuid = features[0].properties.CTUID

			} else {
				map.setPaintProperty('ct_fill', 'fill-color', '#fff')
				ctuid = '0'
			}

		});

		map.on('load', function() {
			setMetric(metric);
			if (metric === "population") {
				document.getElementById('metric-population').classList.add('selected-metric');
				document.getElementById('metric-population').classList.remove('not-selected-metric');
				document.getElementById('metric-dwelling').classList.remove('selected-metric');
				document.getElementById('metric-dwelling').classList.add('not-selected-metric');
			} else {
				document.getElementById('metric-population').classList.remove('selected-metric');
				document.getElementById('metric-population').classList.add('not-selected-metric');
				document.getElementById('metric-dwelling').classList.add('selected-metric');
				document.getElementById('metric-dwelling').classList.remove('not-selected-metric');
			}
		});

	});

	

	function placeClick(city) {
		ctuid = "0";
		map.setPaintProperty('ct_fill', 'fill-color', '#fff');
		map.panTo(city.original.geometry.coordinates);
		map.zoonTo(10);
	}

	


</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> 
	<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">

	<link href='https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.css' rel='stylesheet' />
	<link href='popupStyle.css' rel='stylesheet' />
</svelte:head>


<main>

<Header/>

<div id='map-wrapper' class="{pageWidth < 755 ? 'maps-small' : 'maps-big'}" >
	<div id="map" bind:offsetWidth={pageWidth} ></div>
</div>

<div id="metric">
	<!-- <div id="metric-label">
	  <p>Selected Metric</p>
	</div> -->
	<div 
		id="metric-population" 
		class:selected-metric={metric === 'population'}
    	class:non-selected-metric={metric !== 'population'}
		on:click={() => setMetric('population')}>
	  <p>Population →</p>
	</div>
	<div 
		id="metric-dwelling" 
		class:selected-metric={metric === 'dwelling'}
   		class:non-selected-metric={metric !== 'dwelling'}
		on:click={() => setMetric('dwelling')}>
	  <p>Occupied Dwellings →</p>
	</div>
</div>
  

<div id="search">
	<Typeahead
			{data}
			label=""
			inputAfterSelect="clear"
			placeholder={`search and zoom to a city`}
			limit={5}
			extract={(item) => item.properties.GEONAME}
			on:select={({ detail }) => placeClick(detail)}
			let:result
		>
		<span id="search-results">{@html result.string}</span>
	</Typeahead>
</div>

<Select ctuid={ctuid} metric={metric}/>

<Info pageWidth={pageWidth} metric={metric}/>

</main>


<style>
	
	
	@font-face {
		font-family: TradeGothicBold;
		src: url("./assets/Trade Gothic LT Bold.ttf");
	}
	:root {
		font-family: 'Roboto', sans-serif;
	}

	main {
		margin: auto;
		width: 100%;
		margin-bottom: -15px;
	}

	#metric {
		position: absolute;
		bottom: 256px;
		left: 0px;
		height: 21px;
		width: 335px;
		background-color: white;
		border: solid 1px #1E3765;
		border-left: none;
		z-index: 999;
		display: flex;
  		flex-wrap: wrap;
		text-align: center;
	}
	#metric p {
		font-family: Roboto, sans-serif;
		font-size: 13px;
		color: rgb(70, 70, 70);
		margin-top: 2px;
	}
	#metric-label {
		width: 100%;
		height: 21px;
		border-bottom: solid 1px lightgray;
	}
	#metric-population,
	#metric-dwelling {
		width: 50%;
		box-sizing: border-box;
		height: 21px;
		cursor: pointer;
		border: none;
		
	}
	#metric-population {
		order: 1;
		border-right: solid 1px #1E3765;
	}
	#metric-dwelling {
		order: 2;
	}
	#metric-population:hover {
		background-color: #F1C500;
	}
	#metric-dwelling:hover {
		background-color: #F1C500;
	}

	.selected-metric {
		background-color: #F1C500;
		border-bottom: solid 1px #1E3765;
	}
	.non-selected-metric {
		background-color: rgb(225, 225, 225);
	}


	:global([data-svelte-search]) {
		height: 50px;
		border: solid 1px lightgrey;
		border-radius: 0px;
		background-color: none;
		font-size: 10px;
	}
	:global([data-svelte-search] li) {
		height: 50px;
	}
	:global([data-svelte-search] label) {
		display: none;
	}
	:global([data-svelte-typeahead] mark)  {
		color: #1E3765;
		background-color: #F1C500;
	}
	:global(body) {
		padding: 0px;
		margin: 0px;
		background-color: #fff;
	}
	#search-results {
		color: #1E3765;
		font-family: Roboto, sans-serif;
	}
	#search {
		position: absolute;
		width: 260px;
		top: 40px;
		left: 5px;
		z-index: 1;
		opacity: 0.93;
	}

	#map-wrapper {
		margin-top: 50px;
		width: 100%;
		top: 0;
        left: 0;
		position: absolute;
		z-index: -99;
	}

	#map {
		height: 100%;
		width: 100%;
		top: 0;
        left: 0;
		position: absolute;
		z-index: -99;
	}

	.maps-big {
		height: calc(100vh - 50px);
	}

	.maps-small {
		height: calc(100vh - 255px - 50px);
	}

	
</style>
