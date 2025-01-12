# import random
# import os
# import streamlit as st

# # Path to images directory
# vegetable_images_path = r'C:\Users\gurum\Desktop\SpacECE_TASKS\Vegetable_Game\vegetable_images'

# # List of vegetable image filenames (ensure these images exist in the folder)
# vegetable_images = [
#     'brinjal.jpg', 'cabbage.jpg', 'potato.jpg', 'tomato.jpg',
#     'capsicum.jpg', 'onion.jpg', 'carrot.jpg', 'radish.jpg'
# ]

# # Function to display images and ask user to count the vegetables
# def count_vegetables(difficulty='easy'):
#     if 'selected_images' not in st.session_state or 'options' not in st.session_state:
#         # Determine the number of images based on the selected difficulty
#         if difficulty == 'easy':
#             num_images = random.randint(1, 5)  # Show between 1 and 5 images
#         else:
#             num_images = random.randint(6, 10)  # Show between 6 and 10 images
        
#         # Select random images
#         selected_images = random.sample(vegetable_images, num_images)

#         # Store the selected images and their count in session state
#         st.session_state.selected_images = selected_images
#         st.session_state.correct_count = len(selected_images)

#         # Generate 4 unique options (including the correct one)
#         options = set()
#         options.add(st.session_state.correct_count)  # Add the correct answer

#         # Add other options close to the correct one, making sure they are unique
#         while len(options) < 4:
#             random_option = st.session_state.correct_count + random.randint(-1, 2)  # Create options around the correct number
#             options.add(random_option)

#         st.session_state.options = list(options)  # Save the options in session state

#     # Display the selected vegetable images with fixed size (e.g., width = 300px)
#     image_paths = [os.path.join(vegetable_images_path, img) for img in st.session_state.selected_images]
#     for image_path in image_paths:
#         st.image(image_path, width=150)  # Resize each image to 300px width

#     correct_count = st.session_state.correct_count

#     # Display options as radio buttons for user to select with a unique key
#     selected_option = st.radio(
#         "How many vegetables do you see in the above images?", 
#         st.session_state.options, 
#         key=f"radio_button_{st.session_state.correct_count}"  # Unique key based on correct count
#     )

#     # Handle the user's response when they click 'Submit'
#     if st.button('Submit', key="submit_button"):
#         if selected_option == correct_count:
#             st.success(f"Correct! You got it right. There are {correct_count} vegetables!")
#         else:
#             st.error(f"Incorrect. There are {correct_count} vegetables. Try again!")

#     # Continue button to generate a new question
#     if st.button('Continue', key="continue_button"):
#         # Clear the session state for a new question
#         st.session_state.pop('selected_images', None)
#         st.session_state.pop('options', None)
#         st.session_state.pop('correct_count', None)
#         count_vegetables(difficulty=difficulty)  # Regenerate new question

# # Main function to select difficulty level and start the game
# def select_difficulty():
#     # Add Quit button
#     if st.button("Quit", key="quit_button"):
#         st.warning("You have exited the game. Thank you for playing!")
#         st.stop()  # Stops execution of further code

#     difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium"], key="difficulty_radio")
#     count_vegetables(difficulty=difficulty.lower())

# # Streamlit app execution starts here
# st.title("Vegetable Counting Game")

# # Run the game
# select_difficulty()


import random
import os
import streamlit as st

# Path to images directory
vegetable_images_path = r'C:\Users\gurum\Desktop\SpacECE_TASKS\Vegetable_Game\vegetable_images'

# List of vegetable image filenames (ensure these images exist in the folder)
vegetable_images = [
    'brinjal.jpg', 'cabbage.jpg', 'potato.jpg', 'tomato.jpg',
    'capsicum.jpg', 'onion.jpg', 'carrot.jpg', 'radish.jpg'
]

# Function to display images and ask user to count the vegetables
def count_vegetables(difficulty='easy'):
    if 'selected_images' not in st.session_state or 'options' not in st.session_state:
        # Determine the number of images based on the selected difficulty
        if difficulty == 'easy':
            num_images = random.randint(1, 5)  # Show between 1 and 5 images
        else:
            num_images = random.randint(6, 10)  # Show between 6 and 10 images
        
        # Select random images
        selected_images = random.sample(vegetable_images, num_images)

        # Store the selected images and their count in session state
        st.session_state.selected_images = selected_images
        st.session_state.correct_count = len(selected_images)

        # Generate 4 unique options (including the correct one)
        options = set()
        options.add(st.session_state.correct_count)  # Add the correct answer

        # Add other options close to the correct one, making sure they are unique
        while len(options) < 4:
            random_option = st.session_state.correct_count + random.randint(-1, 2)  # Create options around the correct number
            options.add(random_option)

        st.session_state.options = list(options)  # Save the options in session state

    # Display the selected vegetable images in a 3-column grid
    image_paths = [os.path.join(vegetable_images_path, img) for img in st.session_state.selected_images]
    num_columns = 3  # Number of images per row
    cols = st.columns(num_columns)
    
    for idx, image_path in enumerate(image_paths):
        with cols[idx % num_columns]:  # Cycle through columns
            st.image(image_path, width=150)  # Resize each image to 150px width

    correct_count = st.session_state.correct_count

    # Display options as radio buttons for user to select with a unique key
    selected_option = st.radio(
        "How many vegetables do you see in the above images?", 
        st.session_state.options, 
        key=f"radio_button_{st.session_state.correct_count}"  # Unique key based on correct count
    )

    # Handle the user's response when they click 'Submit'
    if st.button('Submit', key="submit_button"):
        if selected_option == correct_count:
            st.success(f"Correct! You got it right. There are {correct_count} vegetables!")
        else:
            st.error(f"Incorrect. There are {correct_count} vegetables. Try again!")

    # Continue button to generate a new question
    if st.button('Continue', key="continue_button"):
        # Clear the session state for a new question
        st.session_state.pop('selected_images', None)
        st.session_state.pop('options', None)
        st.session_state.pop('correct_count', None)
        # count_vegetables(difficulty=difficulty)  # Regenerate new question
        st.experimental_rerun() 

# Main function to select difficulty level and start the game
def select_difficulty():
    # Add Quit button
    if st.button("Quit", key="quit_button"):
        st.warning("You have exited the game. Thank you for playing!")
        st.stop()  # Stops execution of further code

    difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium"], key="difficulty_radio")
    count_vegetables(difficulty=difficulty.lower())

# Streamlit app execution starts here
st.title("Vegetable Counting Game")

# Run the game
select_difficulty()
