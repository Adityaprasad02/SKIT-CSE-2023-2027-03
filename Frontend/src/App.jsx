import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import AuthLayout from "./layouts/AuthLayout";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ForgotPassword from "./pages/ForgotPassword";

function App() {
  return (
    <BrowserRouter>

<Routes>

{/* Public Website */}
<Route element={<MainLayout />}>
  <Route path="/" element={<Home />} />
</Route>

{/* Authentication */}
<Route element={<AuthLayout />}>

  <Route
    path="/login"
    element={<Login />}
  />

  <Route
    path="/signup"
    element={<Signup />}
  />

  <Route
    path="/forgot-password"
    element={<ForgotPassword />}
  />

</Route>

</Routes>

    </BrowserRouter>
  );
}

export default App;