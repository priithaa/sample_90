import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score 

def main():
    st.title("Binary Classification Web App")
    st.sidebar.title("Binary Classification Web App")
    st.markdown("Are Your Mushrooms edible or poisonous?")
    # st.markdown("Are Your Mushrooms edible or poisonous?")
    st.sidebar.markdown("Are Your Mushrooms edible or poisonous?")

    @st.cache(persist=True)
    def load_data():
        data=pd.read_csv("/home/rhyme/Desktop/Project/mushrooms.csv")
        label=LabelEncoder()

        for col in data.columns:
            data[col]=label.fit_transform(data[col])
        return data 

    @st.cache(persist=True)
    def split(df):
        y = df.type 
        x = df.drop(columns= ['type'])
        x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3, random_state= 0)

        return x_train, x_test, y_train, y_test

    def plot_metrics(metrics_list):
        if 'Confusion Marix' in metrics_list:
            st.subheader("Confusion Matrix")
            plot_confusion_matrix(model, x_test, y_test, display_labels= class_names)
            st.pyplot()

        if 'ROC Curve' in metrics_list:
            st.subheader("ROC Curve")
            plot_roc_curve(model, x_test, y_test)
            st.pyplot()

        if "Precision-Recall Curve" in metrics_list:
            st.subheader("Precision-recall Curve")
            plot_precision_recall_curve(model, x_test,y_test)
            st.pyplot()


    df= load_data()
    x_train, x_test, y_train, y_test = split(df)
    # st.write(x_train, x_test, y_train, y_test)
    class_names = ['edible', 'poisonous']

    st.sidebar.subheader("Choose Classifier")
    classifier = st.sidebar.selectbox("Classifier", ("Support vector Machine (SVM)", "Logistic Regression", "Random Forrest"))

    if classifier == 'Support vector Machine (SVM)':
        st.sidebar.subheader("Model Hyperparameters")
        C = st.sidebar.number_input("C (Regularisation Parameter)", 0.01, 10.0, step=0.01, key='C')
        kernel = st.sidebar.radio("Kernel", ("rbf", "linear"), key='kernel')
        gamma = st.sidebar.radio("Gamma", ("scale", "auto"), key='gamma')

        metrics = st.sidebar.multiselect("What metrics to plot?", ("Confusion Marix","ROC Curve", "Precision-Recall Curve"))

        if st.sidebar.button("Classify",key='classify'):
            st.sidebar.subheader("Support Vector Machine (SVC) Results")
            model = SVC(C=C, kernel=kernel, gamma=gamma)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision:", precision_score(y_test, y_pred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
            plot_metrics(metrics)


    if classifier == 'Logistic Regression':
        st.sidebar.subheader("Model Hyperparameters")
        C = st.sidebar.number_input("C (Regularisation Parameter)", 0.01, 10.0, step=0.01, key='C_LR')
        max_iter = st.sidebar.slider("Mximum Number of Iterations", 100, 500, key='max_iter')
        # gamma = st.sidebar.radio("Gamma", ("scale", "auto"), key='gamma')

        metrics = st.sidebar.multiselect("What metrics to plot?", ("Confusion Marix","ROC Curve", "Precision-Recall Curve"))

        if st.sidebar.button("Classify",key='classify'):
            st.sidebar.subheader("Logistic Regression Results")
            model = LogisticRegression(C=C, max_iter=max_iter)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision:", precision_score(y_test, y_pred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
            plot_metrics(metrics)


    if classifier == 'Random Forrest':
        st.sidebar.subheader("Model Hyperparameters")
        n_estimators = st.sidebar.number_input("The Number of trees", 100, 500, step=10, key='n_estimators')
        # max_iter = st.sidebar.slider("Mximum Number of Iterations", 100, 500, key='max_iter')
        max_depth= st.sidebar.number_input("the maximum depth of the tree", 1 ,10, step=1, key="depth")
        bootstrap=st.sidebar.radio("Bootstrap samples when building trees", ('True', 'False'), key='bootstrap')
        # gamma = st.sidebar.radio("Gamma", ("scale", "auto"), key='gamma')

        metrics = st.sidebar.multiselect("What metrics to plot?", ("Confusion Marix","ROC Curve", "Precision-Recall Curve"))

        if st.sidebar.button("Classify",key='classify'):
            st.sidebar.subheader("Random Forest Results")
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap=bootstrap, n_jobs=-1)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision:", precision_score(y_test, y_pred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
            plot_metrics(metrics)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    if st.sidebar.checkbox("Show Raw Data", False):
        st.subheader("Mushroom Data Set (Classification)")
        st.write(df)






if __name__ == '__main__':
    main()


