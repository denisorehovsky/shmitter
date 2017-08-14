module Route exposing
  ( Route(..)
  , modifyUrl
  , parseLocation
  )

import Navigation exposing (Location)
import UrlParser as Url exposing ((</>), Parser, oneOf, parseHash, s, top, string)


-- ROUTING


type Route
  = Home
  | Login


matchers : Parser (Route -> a) a
matchers =
  oneOf
    [ Url.map Home top
    , Url.map Login (s "login")
    ]


routeToString : Route -> String
routeToString route =
  let
    pieces =
      case route of
        Home ->
          []

        Login ->
          [ "login" ]
  in
    "#/" ++ String.join "/" pieces



-- HELPERS


modifyUrl : Route -> Cmd msg
modifyUrl route =
  routeToString route
    |> Navigation.modifyUrl


parseLocation : Location -> Maybe Route
parseLocation location =
  parseHash matchers location
