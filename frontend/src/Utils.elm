module Utils exposing ((=>))


(=>) : a -> b -> ( a, b )
(=>) =
    (,)


infixl 0 =>
