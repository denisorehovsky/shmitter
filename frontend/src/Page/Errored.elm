module Page.Errored exposing
  ( Model
  , view
  )

import Html exposing (Html, div, text)


-- MODEL


type alias Model =
  { errorMessage : String
  }



-- VIEW


view : Model -> Html msg
view model =
  div []
    [ text model.errorMessage
    ]
