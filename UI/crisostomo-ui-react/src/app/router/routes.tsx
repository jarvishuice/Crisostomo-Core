import { Routes, Route } from "react-router-dom";
import { Layout } from "../../shared/components/layout/Layout";
import { Login } from "../../features/auth/pages/Login";
import { Register } from "../../features/auth/pages/Register";
import { PrivateRoute } from "../../features/auth/components/PrivateRoute";
import { BooksPage } from "../../features/books/pages/BooksPage";
import { CreateBookForm } from "../../features/books/components/FormCreateBook";
import CreateBookPage from "../../features/books/pages/CreateBookPage";

// Pages importadas desde features
// import BooksPage from "../../features/books/pages/BooksPage";
// import BookDetailPage from "../../features/books/pages/BookDetailPage";

// import CategoriesPage from "../../features/categories/pages/CategoriesPage";
// import AuthorsPage from "../../features/authors/pages/AuthorsPage";


// Layout general


export default function AppRoutes() {
    return (
        <Routes>
            <Route element={<Layout />}>
                {/* libros */}
                <Route path="/books" element={<PrivateRoute><BooksPage></BooksPage></PrivateRoute>} />
               <Route  path="/addBook" element = {<PrivateRoute><CreateBookPage></CreateBookPage></PrivateRoute>}/>

                {/* Home */}
                <Route path="/" element={<PrivateRoute><h1>Bienvenido</h1></PrivateRoute>} />
            </Route>
            <Route path="/login" element={<Login/>}/>
            <Route path="/Register" element={<Register/>}/>

            
        </Routes>
    );
}
