import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Pages/HomePage';
import { CartProvider } from './Context/CartContext.tsx';
import AdminPage from './Pages/AdminPage';

function App() {
  return (
    <CartProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={ <AdminPage />} />
        </Routes>
      </Router>
    </CartProvider>
  );
}

export default App;