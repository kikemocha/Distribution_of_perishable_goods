import React, { createContext, useContext, useReducer, useEffect } from "react";
import { Product } from "../types";

// Define la interfaz para el estado del carrito
interface CartState {
  products: Product[];
}

// Acciones del carrito
type CartAction =
  | { type: 'ADD_TO_CART'; product: Product }
  | { type: 'REMOVE_FROM_CART'; productId: number }
  | { type: 'CLEAR_CART' };

// Estado inicial del carrito
const initialState: CartState = {
  products: [],
};

// Reducer del carrito
const cartReducer = (state: CartState, action: CartAction): CartState => {
  switch (action.type) {
    case 'ADD_TO_CART':
      const existingProduct = state.products.find(p => p.id === action.product.id);
      if (existingProduct) {
        return {
          ...state,
          products: state.products.map(p =>
            p.id === action.product.id
              ? { ...p, userQuantity: (p.userQuantity || 0) + (action.product.userQuantity || 0) }
              : p
          ),
        };
      } else {
        return {
          ...state,
          products: [...state.products, action.product],
        };
      }
    case 'REMOVE_FROM_CART':
      return {
        ...state,
        products: state.products.filter(p => p.id !== action.productId),
      };
    case 'CLEAR_CART':
      return initialState;
    default:
      return state;
  }
};

// Crear el contexto
const CartContext = createContext<{
  state: CartState;
  dispatch: React.Dispatch<CartAction>;
}>({
  state: initialState,
  dispatch: () => null,
});

// Proveedor del contexto
export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Cargar el estado inicial desde sessionStorage
  const [state, dispatch] = useReducer(cartReducer, initialState, (initial) => {
    const storedState = sessionStorage.getItem("cartState");
    return storedState ? JSON.parse(storedState) : initial;
  });

  // Guardar el estado en sessionStorage cuando cambie
  useEffect(() => {
    sessionStorage.setItem("cartState", JSON.stringify(state));
  }, [state]);

  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
};

// Hook personalizado para usar el contexto
export const useCart = () => useContext(CartContext);
