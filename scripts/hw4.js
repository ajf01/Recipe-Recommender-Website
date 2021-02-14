// Global constants
const DEBUG = true;
const DINGUS_PRICE = 14.25;
const WIDGET_PRICE = 9.99;

// Some little helpers
const log = msg => (DEBUG ? console.log(msg) : '');
const select = id => document.getElementById(id);

function plotMap(sales) {
    dataSales = sales;
    var data = [
        {
            'CONTINENT': 'North America',
            'hc-middle-x': 0.22,
            'hc-middle-y': 0.5
        },
        {
            'CONTINENT': 'Asia',
            'hc-middle-x': 0.75,
            'hc-middle-y': 0.4
        },
        {
            'CONTINENT': 'South America',
            'hc-middle-x': 0.65,
            'hc-middle-y': 0.33
        },
        {
            'CONTINENT': 'Antarctica',
            'hc-middle-x': 0.57,
            'hc-middle-y': 0.82
        },
        {
            'CONTINENT': 'Australia',
            'hc-middle-x': 0.48,
            'hc-middle-y': 0.35
        },
        {
            'CONTINENT': 'Europe',
            'hc-middle-x': 0.5,
            'hc-middle-y': 0.7
        },
        {
            'CONTINENT': 'Africa',
            'hc-middle-x': 0.45,
            'hc-middle-y': 0.25
        }
    ];
    let originalColor;
    let continents = '../data/continents.json';
    Highcharts.getJSON(continents, function (geojson) {
    
        // Initiate the chart
        Highcharts.mapChart('myMap', {
            chart: {
                type: 'map',
                zoomType: 'None',
                enableMouseWheelZoom: false,
                panning: false
            },
            title: {
                text: null
            },
            mapNavigation: {
                enabled: false,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },
            tooltip: {
                formatter: function() {
                    return this.point.properties.CONTINENT.toUpperCase();
                },
                borderRadius: 10,
                borderWidth: 0.5,
                borderColor: 'black',
                backgroundColor: 'white'
            },
            plotOptions: {
                series: {
                    point: {
                        cursor: 'pointer',
                        events: {
                            click: function () {
                                plotColumn(this.CONTINENT.replace(/\s+/g, '').toUpperCase());
                                plotPie(this.CONTINENT.replace(/\s+/g, '').toUpperCase());
                                updateScoreCards(this.CONTINENT.replace(/\s+/g, '').toUpperCase());
                            },
                            mouseOver: function() {
                                originalColor = this.color;
                                if (this.state == 'select'){
                                    this.update({
                                        color: '#0C3'
                                    });
                                }
                            },
                            mouseOut: function() {
                                if (this.color == '#0C3'){
                                    this.update({
                                        color: originalColor
                                    });
                                }
                            }
                        }
                    },
                }
            },
            exporting: { 
                enabled: false 
            },
            series: [{
                data: data,
                mapData: geojson,
                showInLegend: false,
                color: '#dddddd',
                keys: ['CONTINENT', 'hc-middle-x', 'hc-middle-y'],
                joinBy: 'CONTINENT',
                name: null,
                allowPointSelect: true,
                cursor: 'pointer',
                states: {
                    select: {
                        color: '#7CA82B'
                    },
                    hover: {
                        color: '#C4C4C4'
                    }
                },
                dataLabels: {
                    enabled: true,
                    format: '{point.properties.CONTINENT}',
                    style: {
                        fontSize: 9,
                        fontFamily: 'Lucida Sans Unicode'
                    }
                }
            }],
            credits: {
                enabled: false
            }
        });
    });
}

function plotColumn(continent) {
    let dingusValues = {
        month: [],
		values: []
	}
	let widgetValues = {
        month: [],
		values: []
    }
    let sales = dataSales[continent];
	for (const datum of sales) {
		let month = datum['Month'];
		let dingus = datum['Dingus'];
        let widget = datum['Widget'];
        dingusValues['month'].push(month);
		widgetValues['month'].push(month);
		dingusValues['values'].push(dingus);
		widgetValues['values'].push(widget);
    }
	Highcharts.chart('salesPerMonthChart', {
		chart: {
            type: 'column',
            animation: false
		},
		title: {
            text: 'Monthly Sales',
            style: {
                fontSize: 18,
                fontWeight: 'bold',
                fontFamily: 'Lucida Sans Unicode'
            },
		},
		xAxis: {
			categories: dingusValues['month'],//['January','February','March'],
			title: {
                text: 'Month',
                style: {
                    //fontSize: 9,
                    fontWeight: 'bold',
                    fontFamily: 'Lucida Sans Unicode'
                },
            },
            tickmarkPlacement: 'between',
            tickLength: 5,
            tickWidth: 0.5,
            tickColor: 'black',
            lineColor: 'gray',
            lineWidth: 1
		},
		yAxis: {
            min: 0,
            tickAmount: [3],
            //showLastLabel: true,
            gridLineColor: 'lightgray',
            //gridLineDashStyle: 'ShortDot',
            //height: '100%',
            tickLength: 6,
            tickmarkPlacement: 'on',
            tickWidth: 0.5,
            tickColor: 'black',
            lineWidth: 1,
            lineColor: 'grey',
            visible: true,
			title: {
                text: 'Number of units sold',
                style: {
                    fontWeight: 'bold',
                    fontFamily: 'Lucida Sans Unicode'
                }
			}
        },
		legend: {
            symbolHeight: 11,
            symbolWidth: 11,
            symbolRadius: 0,
            layout: 'vertical',
            itemMarginTop: 3,
            itemMarginBottom: 3,
            align: 'right',
            verticalAlign: 'top',
            borderWidth: 1,
            borderColor: 'lightgray',
            itemStyle: {
                fontSize: 10
            },
            padding: 13,
            symbolPadding: 10,
            //margin: 8,
            //floating: true,
            //y: 10
        },
        plotOptions: {
            series: {
                pointPadding: .05,
                groupPadding: 0.08,
                animation: false,
                states: {
                    hover: {
                        enabled: false
                    },
                    inactive: {
                        opacity: 1
                    }
                }
            }
        },
        exporting: { 
            enabled: false 
        },
        tooltip: {
            useHTML: true,
            formatter: function(){
                return '<div style="background-color:'+this.series.color+'"class="tooltip">'+this.y+'</div>';
            },
            followPointer: true,
            borderWidth: 1,
            padding: 0.5,
            shadow: false,
            //borderRadius: 5,
            //box-shadow: 2 2 2,
            style: {
                color: 'white'
            },
            shape: 'square',
            borderColor: 'white'
        },
		series: [{
            name: 'Dinguses',
            style: {
                fontSize: 9,
                fontFamily: 'Lucida Sans Unicode'
            },
            data: dingusValues['values'],
            color: '#29a2cc'
		}, {
            name: 'Widgets',
            style: {
                fontSize: 9,
                fontFamily: 'Lucida Sans Unicode'
            },
            data: widgetValues['values'],
            color: '#d31e1e'
		}],
        credits: {
            enabled: false
        }
	});
}

function plotPie(continent) {
    let dingusValues = {
		values: []
	}
	let widgetValues = {
		values: []
	}
	let sales = dataSales[continent];
	let dinguses = 0, widgets = 0;
	for (const datum of sales) {
		dinguses += datum['Dingus'];
		widgets += datum['Widget'];
	}
	dingusValues['values'].push(dinguses);
    widgetValues['values'].push(widgets);
	Highcharts.chart('totalSalesChart', {
		chart: {
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false,
            type: 'pie',
            animation: false
		},
		title: {
            text: 'Total Sales',
            style: {
                fontSize: 21,
                fontWeight: 'bold',
                fontFamily: 'Lucida Sans Unicode'
            }
        },
        tooltip: {
            useHTML: true,
            formatter: function(){
                return '<div style="background-color:'+this.color+'"class="tooltip">'+this.y+'</div>';
            },
            borderWidth: 1,
            padding: 0.5,
            shadow: false,
            followPointer: true,
            style: {
                color: 'white'
            },
            shape: 'square',
            //borderRadius: 10,
            borderColor: 'white'
        },
		accessibility: {
			point: {
				valueSuffix: '%'
			}
		},
		plotOptions: {
			pie: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: {
                    enabled: true,
                    format: '{point.percentage:.1f}%',
                    distance: -60,
                    style: {
                        fontSize: 17,
                        color: 'white',
                        fontFamily: 'Lucida Sans Unicode',
                        textOutline: null
                    }
				},
                showInLegend: true,
                startAngle: 90
            },
            series: {
                states: {
                    hover: {
                        enabled: false
                    },
                    inactive: {
                        opacity: 1
                    }
                }
            }
        },
        exporting: { 
            enabled: false 
        },
        legend: {
            symbolHeight: 11,
            symbolWidth: 11,
            symbolRadius: 0,
            layout: 'vertical',
            itemMarginTop: 3,
            itemMarginBottom: 3,
            align: 'right',
            verticalAlign: 'top',
            borderWidth: 1,
            borderColor: 'lightgray',
            itemStyle: {
                fontSize: 10
            },
            padding: 13,
            symbolPadding: 10,
            //margin: 8,
            floating: true
        },
		series: [{
			name: 'Brands',
            colorByPoint: true,
            animation: false,
			data: [{
				name: 'Dinguses',
                y: dingusValues['values'][0],
                color: '#29a2cc'
			}, {
				name: 'Widgets',
                y: widgetValues['values'][0],
                color: '#d31e1e'
            }],
		}],
        credits: {
            enabled: false
        }
    });
    if (continent === 'ANTARCTICA') {
		select('totalSalesChart').removeChild(select('totalSalesChart').childNodes[0]);
	}
}

function updateScoreCards(continent) {
	let sales = dataSales[continent];
	let dinguses = 0, widgets = 0;
	for (const datum of sales) {
		dinguses += datum['Dingus'];
		widgets += datum['Widget'];
	}
	let revenue = DINGUS_PRICE * dinguses + WIDGET_PRICE * widgets;
	select('dingusSold').innerHTML = dinguses;
	select('widgetSold').innerHTML = widgets;
	select('totalSales').innerHTML = revenue.toFixed(2);
}

async function loadJSON(path) {
	let response = await fetch(path);
	let dataset = await response.json(); // Now available in global scope
	return dataset;
}

function plotStocks(stocks) {
	let prices = [];
	for (datum of stocks) {
		//log(datum);
		prices.push([datum['Date'], datum['Adj Close']]);
    }
	Highcharts.chart('stockChart', {
        chart: {
            height: 400,
            zoomType: 'None',
            panning: false
        },
        title: {
            text: 'Dynamic Growth',
            style: {
                fontSize: 20,
                fontWeight: 'bold',
                fontFamily: 'Lucida Sans Unicode'
            }
		},
		subtitle: {
            text: 'Stock Prices of D&W Corp. from 2015-Present',
            style: {
                fontWeight: 'bold',
                fontFamily: 'Lucida Sans Unicode'
            }
        },
        xAxis: {
            type: 'datetime',
            showFirstLabel: true,
            showLastLabel: true,
            //max: 14,
            lineColor: 'grey',
			title: {
                text: 'Date',
                style: {
                    fontWeight: 'bold',
                    fontFamily: 'Lucida Sans Unicode'
                }
            },
            labels: {
                style: {
                    border: 'solid'
                },
                formatter: function() {
                    return Highcharts.dateFormat('%m/%e/%Y', this.value);
                }
            },
            crosshair: {
                width: 1,
                color: 'gray',
                zIndex: 3,
                label: {
                    enabled: true,
                    backgroundColor: 'gray',
                    format: '{value:%m/%d/%y}'
                }
            },
            showFirstLabel: true,
            showLastLabel: true,
            minPadding: 0,
            maxPadding: 0
		},
		yAxis: {
            showLastLabel: true,
            //gridLineColor: 'black',
            gridLineDashStyle: 'ShortDot',
            //height: '100%',
            tickLength: 8,
            tickmarkPlacement: 'on',
            tickWidth: 1,
            tickColor: 'black',
            lineWidth: 1,
            lineColor: 'grey',
            visible: true,
            max: 160,
            tickInterval: 20,
            opposite: false,
			title: {
                text: 'Adj Close Stock Price',
                style: {
                    fontWeight: 'bold',
                    fontFamily: 'Lucida Sans Unicode'
                }
            },
            crosshair: {
                width: 1,
                color: 'gray',
                zIndex: 3,
                label: {
                    enabled: true,
                    backgroundColor: 'DarkCyan',
                    format: '{value:.0f}'
                }
            }
        },
        scrollbar: {
            enabled: false
        },
        rangeSelector: {
            selected: 'max',
            inputEnabled: false,
            buttonTheme: {
                visibility: 'hidden'
            },
            labelStyle: {
                visibility: 'hidden'
            }
        },
        navigator: {
            enabled: false
        },
        exporting: { 
            enabled: false 
        },
        tooltip: {
            //formatter: this.x
            formatter: function() {
               return '$' + this.point.y.toFixed(2);
            },
            //followPointer: true,
            //backgroundColor: this.color,
            //style: {
            //    color: 'white'
            //},
            shape: 'square',
            borderRadius: 10,
            borderWidth: 1,
            borderColor: 'gray'
        },
        series: [{
            name: null,
            showInLegend: false,
            data: prices,
            type: 'area',
            lineWidth: 2,
            lineColor: '#00A5DA',
            color: '#BFDCEB',
            //threshold: null,
            fillOpacity: .5,
            tooltip: {
                valueDecimals: 2
            }
        }],
        /*responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    chart: {
                        height: 300
                    },
                    subtitle: {
                        text: null
                    },
                    navigator: {
                        enabled: false
                    }
                }
            }]
        },*/
        credits: {
            enabled: false
        }
    });
}

function init() {
	salesPromise = loadJSON('../data/sales.json');
	stocksPromise = loadJSON('../data/stocks.json');
	salesPromise.then(function (sales) {
		plotMap(sales);
	});
	stocksPromise.then(function (stocks) {
		plotStocks(stocks);
	});
}

document.addEventListener('DOMContentLoaded', init, false);
