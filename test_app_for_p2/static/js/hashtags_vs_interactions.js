// Populate the dropdown menu

var accountsArr = [
    'aliceandolivia',
    'bananarepublic',
    'burberry',
    'chloe',
    'coach',
    'ferragamo',
    'gucci',
    'majeofficiel',
    'michaelkors',
    'toryburch'
];

var brandsArr = [
    'Alice and Olivia',
    'Banana Republic',
    'Burberry',
    'Chloe',
    'Coach',
    'Ferragamo',
    'Gucci',
    'Maje',
    'Michael Kors',
    'Tory Burch'
];

// Create the all brands option
var optionAll = document.createElement('option');
optionAll.text = 'All Brands';
optionAll.value = 'all';
optionAll.selected;

document.getElementById('selAccount').appendChild(optionAll)

// Loop through all the account names
for (i = 0; i < accountsArr.length; i++){
        
    // Create an option for each name
    var optionEl = document.createElement('option');
    optionEl.text = brandsArr[i];
    optionEl.value = accountsArr[i];
    
    // Add the option to the dropdown
    var selectEl = document.getElementById('selAccount');
    selectEl.appendChild(optionEl);
}  

optionChanged = function(account_selected){
    
    // Fetch data to plot
    Plotly.d3.json(`/hashtag_vs_interaction/${account_selected}`, function(error, plotData){
        if (error) return console.warn(error);
        
        var photosData = plotData[0];
        var videosData = plotData[1];
        var albumsData = plotData[2];

        console.log(photosData);
        console.log(videosData);
        console.log(albumsData);

        // Make chart for photo-type posts
        var trace1 = {
            x: photosData.hashtag_count,
            y: photosData.int_per_follower,
            text: photosData.post_count,
            mode: 'markers',
        };

        var data = [trace1];

        var layout = {
            title: `${account_selected} Photo Posts`,
            xaxis: {
                title: 'Number of Hashtags Used in Caption',
            },
            yaxis: {
                title: 'Average Likes per Post per Follower'
            }
        };

        Plotly.newPlot('photosChart', data, layout)

        // Make chart for video-type posts
        var trace1 = {
            x: videosData.hashtag_count,
            y: videosData.int_per_follower,
            text: videosData.post_count,
            mode: 'markers',
        };

        var data = [trace1];

        var layout = {
            title: `${account_selected} Video Posts`,
            xaxis: {
                title: 'Number of Hashtags Used in Caption',
            },
            yaxis: {
                title: 'Average Views per Video per Follower'
            }
        };

        Plotly.newPlot('videosChart', data, layout)

        // Make chart for album-type posts
        var trace1 = {
            x: albumsData.hashtag_count,
            y: albumsData.int_per_follower,
            text: albumsData.post_count,
            mode: 'markers',
        };

        var data = [trace1];

        var layout = {
            title: `${account_selected} Album Posts`,
            xaxis: {
                title: 'Number of Hashtags Used in Caption',
            },
            yaxis: {
                title: 'Average Likes per Post per Follower'
            }
        };

        Plotly.newPlot('albumsChart', data, layout)


    })
}