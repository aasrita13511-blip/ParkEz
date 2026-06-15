import streamlit as st

from database import *



st.set_page_config(
    page_title="Driver Portal",
    page_icon="🚘"
)



st.title(
"🚘 Driver Portal"
)


st.write(
"Manage assigned valet vehicles."
)



bookings = all_bookings()



if bookings:


    for row in bookings:



        st.container()


        st.subheader(
        f"Ticket: {row[1]}"
        )



        st.write(
        f"""
        Customer:

        {row[2]}


        Phone:

        {row[3]}


        Vehicle:

        {row[4]}


        Number Plate:

        {row[5]}


        Current Status:

        {row[8]}
        """
        )



        col1,col2,col3 = st.columns(3)



        with col1:


            if st.button(
                "Vehicle Picked",
                key=row[1]+"pick"
            ):


                update_status(
                row[1],
                "Vehicle Picked"
                )


                st.success(
                "Updated"
                )




        with col2:


            if st.button(
                "Vehicle Parked",
                key=row[1]+"park"
            ):


                update_status(
                row[1],
                "Vehicle Parked"
                )


                st.success(
                "Updated"
                )





        with col3:


            if st.button(
                "Delivered",
                key=row[1]+"done"
            ):


                update_status(
                row[1],
                "Delivered"
                )


                st.success(
                "Vehicle Delivered"
                )


        st.divider()



else:


    st.info(
    "No active valet requests"
    )