module Page.Home exposing (..)

import Html exposing (Html, div, text)

import Data.Token as Token exposing (Token)
import Data.User as User exposing (User)
import Utils exposing ((=>))


-- MODEL


type alias Model =
  { user : String
  }


-- init :
-- init =



-- UPDATE


type Msg
  = NoOp


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    NoOp ->
      model => Cmd.none



-- VIEW


view : Model -> Html Msg
view model =
  div [] [ text "Home page" ]
