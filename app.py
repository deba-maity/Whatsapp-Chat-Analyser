import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import seaborn as sns


 # tried for emoji
# import matplotlib.font_manager as fm
#
# font_path = r'NotoColorEmoji-Regular.ttf'
# prop = fm.FontProperties(fname=font_path)
# plt.rcParams['font.family'] = prop.get_name()

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

# adding colorful matplotlib graphs
x_colors = {'A': 10, 'B': 20, 'C': 30, 'D': 40}
light_colors = LinearSegmentedColormap.from_list("light_gradient", ["lightblue", "lightgreen", "yellow"])
colors = light_colors(np.linspace(0, 1, len(x_colors)))

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # unique users fetch karta hai for a grp chat
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    if st.sidebar.button("See chats? click me !"):
        st.dataframe(df)
        st.text(user_list)

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)



    st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(to right, #C33764, #1D2671);  /* Set your desired gradient colors */
    }
    .stApp {
        background: linear-gradient(to right, #C33764, #1D2671);  /* Same gradient for consistency */
    }
    .stButton > button {
        background: linear-gradient(90deg, #A9F1DF, #FFBBBB);  
        color: black;                                          
        border: none;                                        
        padding: 10px 20px;                               
        border-radius: 25px;                                
        font-size: 16px;                                   
        cursor: pointer;                                     
        transition: background 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #4E65FF, #92EFFD); /* Hover gradient */
        color: white;                                        /* Text color on hover */
    }
    .smaller-font {
        font-size:25px !important;
    }
    .small-font {
        font-size:38px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .medium-font {
        font-size:50px !important;
        color:#6bf92a
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .big-font {
        font-size:80px !important; 
        color:#FFC371
    }
    .semi-big-font {
        font-size:65px !important; 
        color:#FFC371
    }
    </style>
    """, unsafe_allow_html=True)

    # analysis = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Original image</p>'
    # st.markdown(analysis, unsafe_allow_html=True)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)

        st.markdown('<p class="big-font">Here is your analysis</p>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<p class="smaller-font">Total messages</p>', unsafe_allow_html=True)
            st.title(num_messages)
        with col2:
            st.markdown('<p class="smaller-font">Total words</p>', unsafe_allow_html=True)
            st.title(words)
        with col3:
            st.markdown('<p class="smaller-font">Media shared</p>', unsafe_allow_html=True)
            st.title(num_media_messages)
        with col4:
            st.markdown('<p class="smaller-font">Links</p>', unsafe_allow_html=True)
            st.title(num_links)


        #timeline
        st.markdown('<p class="medium-font">Monthly Timeline</p>', unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('lightblue')
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily time
        st.markdown('<p class="medium-font">Daily Timeline</p>', unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#f76f6f')
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.markdown('<p class="semi-big-font">Activity Maps</p>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)

        with col1:
            st.markdown('<p class="small-font">Most Busy day</p>', unsafe_allow_html=True)
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            fig.patch.set_facecolor('#f7ab6f')
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown('<p class="small-font">Most Busy Month</p>', unsafe_allow_html=True)
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#f7ed6f')
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown('<p class="medium-font">Weekly activity map</p>', unsafe_allow_html=True)
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        fig.patch.set_facecolor('#c0c4be')
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        if selected_user == 'Overall':
            st.title('Most busy Users')
            x,new_df = helper.most_busy_users(df)
            fig ,ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                fig.patch.set_facecolor('#aafd80')
                ax.bar(x.index, x.values , color = colors)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title('Word cloud')
        df_wc = helper.create_wordcloud(selected_user , df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most common words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig , ax = plt.subplots()
        fig.patch.set_facecolor('#A9F1DF')
        ax.barh(most_common_df[0] , most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df.head(10))

        with col2:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#FFBBBB')
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)






