<script>

    import ct from "../assets/ct.geo.json";

    export let ctuid;
    export let metric;

    let value21 = 0;
    let value96 = 0;
    let radius = 1;
    let stroke = "#fff";
    let fill = "#fff";

    let metricText = "Population";

    $: data = ct.features.filter(ct => ct.properties.ctuid === ctuid)[0];

    $: if (data) {
        if (metric === "population") {
            value21 = Math.round(data.properties.pop_2021 / 10) * 10;
            value96 = Math.round(data.properties.pop_1996 / 10) * 10;
            metricText = "Population";
        } else {
            value21 = Math.round(data.properties.dwe_2021 / 10) * 10;
            value96 = Math.round(data.properties.dwe_1996 / 10) * 10;
            metricText = "Dwellings";
        }
        
        if (value21 > value96) {
            radius = 1 + 2 * ((value21 - value96) / 250) ** 0.5
            stroke = '#007fa3'
            fill = '#6fc7ea'
        } 
        else if (value96 > value21) {
            radius = 1 + 2 * ((value96 - value21) / 250) ** 0.5
            stroke = '#dc4633'
            fill = '#ff5842'
        } else {
            radius = 1;
            stroke = "#fff";
            fill = "#fff";
        }
    } else {
        value21 = 0;
        value96 = 0;
    }

</script>


<div id="select" class="{ctuid !== "0" ? 'show' : 'empty'}">
	<div id="yellow"></div>

    <div id="info">
        <div id="circle">
            <svg width="60" height="60">
                <rect width="60" height="60" style="fill-opacity:1; stroke-width:2; stroke:#8d6d6d; fill:#F1C500" />
                {#if data}
                <circle cx="30" cy="30" r={radius} stroke-width="1" stroke={stroke} fill={fill} />
                {/if}
            </svg>            
        </div>
        <div id="data">
            {#if data}
                <p>{metricText} 2021: <span id="bold">{value21.toLocaleString("en-US")}</span></p>
                <p>{metricText} 1996: <span id="bold">{value96.toLocaleString("en-US")}</span></p>
                <p>Difference: <span id="bold">{(value21 - value96).toLocaleString("en-US")}</span></p>
            {:else}
                <p>Missing data</p>
            {/if}

        </div>
        <p>
            For some areas, data for 1996 are estimated via areal interpolation due to tract boundaries changing over time, and thus may not by 100% accurate.
        </p>
    </div>
</div>



<style>
    #select {
		position: absolute;
		width: 255px;
        height: 135px;
		background-color: #fff;
		border: solid 2px rgb(225, 225, 225);
		border-radius: 4px;
		top: 107px;
		left: 6px;
		z-index: 1;
		opacity: 0.93;
	}
    .empty {display:none}
    
    #info p {
        padding-top: 5px;
        font-size: 10px;
        line-height: 1.2;
        color: rgb(70, 70, 70);
		font-family: Roboto, sans-serif;
        padding-left: 15px;
        padding-right: 10px;
        opacity: 0.6;
    }
	#yellow {
		width: 100%;
		height: 3px;
		padding-top: 4px;
		background-color: #F1C500;
	}
	#circle {
        float:left;
        height: 60px;
        width: 60px;
        background-color: red;
        margin-left: 15px;
        margin-right: 10px;
    }
    #data {
        text-align: right;
        margin-right: 15px;
        min-height: 60px;
    }
    #data p {
		padding-left: 10px;
		color: rgb(70, 70, 70);
		font-family: Roboto, sans-serif;
		font-size: 13px;
		line-height: 0.3;
        opacity: 0.99;
	}
    #bold {
        font-weight: bold;
        color: black;
    }
</style>
