module Page.Errored exposing
  ( Model
  , view
  )

import Html exposing (Html, div, h1, h2, section, text)
import Html.Attributes exposing (class)


-- MODEL


type alias Model =
  { errorMessage : String
  }



-- VIEW


view : Model -> Html msg
view model =
  section [ class "section is-fullwidth" ]
    [ section [ class "hero is-medium is-danger" ]
      [ div [ class "hero-body" ]
        [ div [ class "container" ]
          [ h1 [ class "title" ]
            [ text "Error" ]
          , h2 [ class "subtitle" ]
            [ text model.errorMessage ]
          ]
        ]
      ]
    ]
