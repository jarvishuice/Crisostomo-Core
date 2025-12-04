import { Routes, Route } from "react-router-dom";
import { Layout } from "../../shared/components/layout/Layout";
import { Login } from "../../features/auth/pages/Login";
import { Register } from "../../features/auth/pages/Register";
import { PrivateRoute } from "../../features/auth/components/PrivateRoute";

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
                <Route path="/books" element={<PrivateRoute><h3>holamuenod</h3></PrivateRoute>} />
               

                {/* Home */}
                <Route path="/" element={<h1>Bienvenido</h1>} />
            </Route>
            <Route path="/login" element={<Login/>}/>
            <Route path="/Register" element={<Register/>}/>

            
        </Routes>
    );
}
