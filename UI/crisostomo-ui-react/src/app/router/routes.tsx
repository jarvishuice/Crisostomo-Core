import { Routes, Route } from "react-router-dom";
import { Layout } from "../../shared/components/layout/Layout";
import { Login } from "../../features/auth/pages/Login";
import { Register } from "../../features/auth/pages/Register";
import { PrivateRoute } from "../../features/auth/components/PrivateRoute";
import { BooksPage } from "../../features/books/pages/BooksPage";
import CreateBookPage from "../../features/books/pages/CreateBookPage";
import { ReadBook } from "../../features/books/pages/ReadBook";
import EditorialesPage from "../../features/editorials/pages/EditorialPage";


// Layout general


export default function AppRoutes() {
    return (
        <Routes>
            <Route element={<Layout />}>
                {/* libros */}
                <Route path="/books" element={<PrivateRoute><BooksPage></BooksPage></PrivateRoute>} />
               <Route  path="/addBook" element = {<PrivateRoute><CreateBookPage></CreateBookPage></PrivateRoute>}/>
               <Route path="/read/:code/:name" element={<ReadBook />} />
               {/* Editoriales*/}
               <Route path="/editorials" element={<PrivateRoute><EditorialesPage></EditorialesPage></PrivateRoute>} />
                {/* Home */}
                <Route path="/" element={<PrivateRoute><h1>Bienvenido</h1></PrivateRoute>} />
            </Route>
            <Route path="/login" element={<Login/>}/>
            <Route path="/Register" element={<Register/>}/>

            
        </Routes>
    );
}
