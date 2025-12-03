import { Routes, Route } from "react-router-dom";
import { Layout } from "../../shared/components/layout/Layout";

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
                <Route path="/books" element={<h3>holamuenod</h3>} />
               

                {/* Home */}
                <Route path="/" element={<h1>Bienvenido</h1>} />
            </Route>
        </Routes>
    );
}
