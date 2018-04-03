Plotly.d3.json('accounts_overview_get_data', function(error, plotData){
    if (error) {console.warn(error)};

    // Plot the followers chart
    var traceFollower = {
        x: plotData.account_names,
        y: plotData.follower_counts,
        name: 'Followers',
        type: 'bar',
    }

    var data = [traceFollower]

    var layout = {
        title: 'Number of Followers by Account',
    }

    Plotly.newPlot('followersChart', data, layout)

    // Plot the following chart
    var traceFollowing = {
        x: plotData.account_names,
        y: plotData.following_counts,
        name: 'Followings',
        type: 'bar',
        marker: {
            color: 'rgb(148, 103, 189)'
        }
    }

    var data = [traceFollowing]

    var layout = {
        title: 'Number of Accounts Followed by Account'
    }

    Plotly.newPlot('followingChart', data, layout)

    // Plot the posts chart
    var tracePost = {
        x: plotData.account_names,
        y: plotData.post_counts,
        name: 'Posts',
        type: 'bar',
        marker: {
            color: '#d62728'
        }
    }

    var data = [tracePost]

    var layout = {
        title: 'Total Number of Posts by Account'
    }

    Plotly.newPlot('postsChart', data, layout)

})