import streamlit as st
import pandas as pd

# Initialize session state for books if not already set
if 'library' not in st.session_state:
    st.session_state.library = []

def add_book(title, author, year, genre, read_status):
    book = {
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read_status
    }
    st.session_state.library.append(book)
    st.success(f'Book "{title}" added successfully!')
    st.toast("Book added successfully!",icon="✅")

def remove_book(title):    
    books = [book for book in st.session_state.library if book["Title"].lower() != title.lower()]
    if len(books) == len(st.session_state.library):
        st.error("Book not found")
    else:
        st.session_state.library = books
        st.success(f'Book "{title}" removed successfully!')
        st.toast("Book removed successfully!",icon="❌")

def search_books(query):
    results = [book for book in st.session_state.library if query.lower() in book["Title"].lower() or query.lower() in book["Author"].lower()]
    return results

def get_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["Read"])
    percentage_read = (read_books/total_books) * 100 if total_books > 0 else 0
    return total_books, percentage_read, read_books

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"])

if menu == "Add a Book":
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    if st.button("Add Book"):
        add_book(title, author, year, genre, read_status)

elif menu == "Remove a Book":
    title_to_remove = st.text_input("Enter the book's title to remove")
    if st.button("Remove book"):
        remove_book(title_to_remove)

elif menu == "Search for a Book":
    search_query = st.text_input("Enter book's title or author")
    if st.button("Search"):
        results = search_books(search_query)
        if results:
            st.write(pd.DataFrame(results))
        else:
            st.warning("No such book found!")

elif menu == "Display All Books":
    if st.session_state.library:
        st.write(pd.DataFrame(st.session_state.library))
    else:
        st.info("Your library is empty!")

elif menu == "Display Statistics":
    total_books, percentage_read, read_books = get_statistics()
    st.write(f"📖 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books}")
    st.info(f"⁂ **Percentage Read:** {percentage_read:.2f}%")

elif menu == "Exit":
    with st.popover("Exit"):
        st.markdown("Bye Bye 👋")
    st.balloons()
