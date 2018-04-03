# Import Dependencies
from flask import (Flask, render_template, jsonify, request)
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Set up flask
app = Flask(__name__)

# Initiate datebase session
engine = create_engine('sqlite:///data/unified_db.sqlite')
print('Connected to DB')
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
Posts = Base.classes.posts
Accounts = Base.classes.accounts

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/goals')
def goals_page():
    return render_template('goals.html')

@app.route('/conclusion')
def conclusion_page():
    return render_template('conclusion.html')

@app.route('/accounts_overview')
def accounts_overview_page():
    return render_template('accounts_overview.html')

@app.route('/hashtag_vs_interaction')
def hashtag_vs_interactions_page():
    return render_template('hashtag_count_vs_interaction.html')

@app.route('/frequency_vs_interaction')
def frequency_vs_interactions_page():    
    return render_template('frequency_vs_interactions.html')

@app.route('/day_of_the_week_vs_post_count')
def day_of_the_week_vs_post_count_page():
    return render_template('day_of_the_week_vs_post_count.html')

@app.route('/accounts_overview_get_data')
def accounts_overview_get_data():
    # This data comes from the Accounts table
    account_query = session.query(Accounts).all()

    # Load the account names and numerical counts   
    overview_data = {
        'account_names': [each.account_name for each in account_query],
        'follower_counts': [each.follower_count for each in account_query],
        'following_counts': [each.following_count for each in account_query],
        'post_counts': [each.post_count for each in account_query]
    }
        
    return jsonify(overview_data)

@app.route('/hashtag_vs_interaction/<account_selected>')
def hashtag_vs_interactions_data(account_selected):
    hashtags_vs_int_list = []

    # One set of data for each post type
    for type_selected in ['photo', 'video', 'album']:
        
        # Query the data decided by user selection
        type_query = session.query(Posts).filter_by(post_type=f'{type_selected}')

        if account_selected == 'all':
            account_query = type_query
        else:
            account_query = type_query.filter_by(account_name=f'{account_selected}')
        
        # Format the data from query
        hashtag_counts = [post.hashtag_count for post in account_query.all()]
        follower_counts = [post.account_follower_count for post in account_query.all()]

        # Format the data from query
        hashtag_counts = [post.hashtag_count for post in account_query.all()]
        follower_counts = [post.account_follower_count for post in account_query.all()]

        # Use interaction_count for both likes and views
        interaction_counts_list = []
        for post in account_query.all():
            interaction_count = post.view_count
            if interaction_count == None:
                interaction_count = post.like_count
            interaction_counts_list.append(interaction_count)

        # Calculate interaction per follower
        interaction_per_follower_list = [
            interaction_counts_list[i]/follower_counts[i] \
            for i in range(0, len(account_query.all()))
        ]
        
        # Aggregate data for plotting
        intermediate_df = pd.DataFrame({
            'hashtag_count': hashtag_counts,
            'interaction_per_follower': interaction_per_follower_list
        })

        to_plot_df = intermediate_df.groupby('hashtag_count').mean()
        to_plot_df.rename(columns={'interaction_per_follower': 'avg_interactions_per_follower'}, inplace=True)
        to_plot_df['post_count'] = intermediate_df.groupby('hashtag_count').count()
        
        # Save the data in for js retrieval
        to_plot_dict = {
            'post_type': type_selected,
            'hashtag_count': list(map(int, to_plot_df.index.tolist())),
            'int_per_follower': list(map(float, to_plot_df.avg_interactions_per_follower.tolist())),
            'post_count': list(map(int, to_plot_df.post_count.tolist()))
        }

        hashtags_vs_int_list.append(to_plot_dict)

    return jsonify(hashtags_vs_int_list)

@app.route('/frequency_vs_interaction_get_data')
def frequency_vs_interactions_data():
    # Query data and store for processing
    post_query = session.query(Posts).all()

    bubble_data = {
            'account_name': [each.account_name for each in post_query],
            'account_follower_count': [each.account_follower_count for each in post_query],
            'post_datetime': [each.post_datetime for each in post_query],
            'like_count': [each.like_count for each in post_query],
            'view_count': [each.view_count for each in post_query]
        }

    bubble_df = pd.DataFrame(bubble_data)

    # Aggregate data for plotting
    grouped_df = pd.DataFrame(bubble_df.groupby('account_name').sum())
    grouped_df.account_follower_count = bubble_df.groupby('account_name')['account_follower_count'].mean()
    grouped_df

    # Calculate the number of days included in the data for each account
    days_counts = []

    def get_day_count(timedelta):
        return ((timedelta.total_seconds() / 60) / 60) / 24

    for index in grouped_df.index:
        # Select all datetimes of given account
        account_datetimes = bubble_df[bubble_df['account_name'] == index].post_datetime
        # Calculate the number of days
        account_timedelta = account_datetimes.max() - account_datetimes.min()
        days_count = get_day_count(account_timedelta)
        
        days_counts.append(days_count)

    # Populate df with all relevant data
    grouped_df['days_count'] = days_counts

    grouped_df['post_count'] = bubble_df.groupby('account_name')['post_datetime'].count()

    grouped_df['post_per_day'] = [
        grouped_df.post_count[i] / grouped_df.days_count[i] \
        for i in range(0, len(grouped_df))
    ]

    grouped_df['like_per_follower'] = [
        grouped_df.like_count[i] / grouped_df.account_follower_count[i] \
        for i in range(0, len(grouped_df))
    ]

    grouped_df['view_per_follower'] = [
        grouped_df.view_count[i] / grouped_df.account_follower_count[i] \
        for i in range(0, len(grouped_df))
    ]
    
    grouped_df['interaction_count'] = [
        grouped_df.view_count[i] + grouped_df.like_count[i] \
        for i in range(0, len(grouped_df))
    ]

    grouped_df['int_per_follower'] = [
        grouped_df.interaction_count[i] / grouped_df.account_follower_count[i] \
        for i in range(0, len(grouped_df))
    ]

    # Store relevant data in jsonifiable format
    to_graph_data = {
        'account_name': grouped_df.index.tolist(),
        'post_count': grouped_df.post_count.tolist(),
        'post_per_day': grouped_df.post_per_day.tolist(),
        'follower_count': grouped_df.account_follower_count.tolist(),
        'like_per_follower': grouped_df.like_per_follower.tolist(),
        'view_per_follower': grouped_df.view_per_follower.tolist(),
        'int_per_follower': grouped_df.int_per_follower.tolist()
    } 

    return jsonify(to_graph_data)

@app.route('/day_of_the_week_vs_post_count/<account_selected>')
def day_of_the_week_vs_post_count_data(account_selected):
    # Query data based on account selection
    if account_selected == 'all':
        post_query = session.query(Posts).all()
    else:
        post_query = session.query(Posts).filter_by(account_name=account_selected).all()

    # Store data in df
    post_datetime = [post.post_datetime for post in post_query]
    like_count = [post.like_count for post in post_query]
    view_count = [post.view_count for post in post_query]

    query_df = pd.DataFrame({
        'post_datetime': post_datetime,
        'like_count': like_count,
        'view_count': view_count
    })

    # Render weekday
    query_df['weekday'] = [datetime.weekday() for datetime in query_df.post_datetime]

    # Aggregate data for plotting
    grouped_df = pd.DataFrame(query_df.groupby('weekday').sum())
    grouped_df['post_count'] = query_df.groupby('weekday').post_datetime.count()
    grouped_df.rename(columns={'like_count': 'total_likes', 'view_count': 'total_views'}, inplace=True)
    grouped_df['avg_likes'] = query_df.groupby('weekday').like_count.mean()
    grouped_df['avg_views'] = query_df.groupby('weekday').view_count.mean()
    grouped_df['photo_or_album_post_count'] = query_df.groupby('weekday').like_count.count()
    grouped_df['video_post_count'] = query_df.groupby('weekday').view_count.count()

    # Convert int64 types to float64 for jsonification
    grouped_df.post_count = grouped_df.post_count.astype(float)
    grouped_df.photo_or_album_post_count = grouped_df.photo_or_album_post_count.astype(float)
    grouped_df.video_post_count = grouped_df.video_post_count.astype(float)

    to_plot_data = {
        'weekday': grouped_df.index.astype(float).tolist(),
        'all_post_count': grouped_df.post_count.tolist(),
        'like_post_count': grouped_df.photo_or_album_post_count.tolist(),
        'view_post_count': grouped_df.video_post_count.tolist(),
        'total_likes': grouped_df.total_likes.tolist(),
        'total_views': grouped_df.total_views.tolist(),
        'avg_likes': grouped_df.avg_likes.tolist(),
        'avg_views': grouped_df.avg_views.tolist()
    }

    return jsonify(to_plot_data)

if __name__ == "__main__":
    app.run(debug=True, port=5037)