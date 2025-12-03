import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes";

const AppRouter = () => {
    return (
        <BrowserRouter>
            <AppRoutes />
        </BrowserRouter>
    );
};

export default AppRouter;
