module Page.NotFound exposing
  ( view
  )

import Html exposing (Html, div, h1, h2, section, text)
import Html.Attributes exposing (class)


-- VIEW


view : Html msg
view =
  section [ class "section is-fullwidth" ]
    [ section [ class "hero is-medium is-danger" ]
      [ div [ class "hero-body" ]
        [ div [ class "container" ]
          [ h1 [ class "title" ]
            [ text "Error" ]
          , h2 [ class "subtitle" ]
            [ text "Page not found :(" ]
          ]
        ]
      ]
    ]
