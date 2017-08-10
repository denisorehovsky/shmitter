module Route exposing
  ( Route(..)
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



-- HELPERS


parseLocation : Location -> Maybe Route
parseLocation location =
  parseHash matchers location
