module Main exposing (..)

import Html exposing (Html, div, text)

import Utils exposing ((=>))


main : Program Never Model Msg
main =
  Html.program
    { init = init
    , view = view
    , update = update
    , subscriptions = \_ -> Sub.none
    }



-- MODEL


type alias Model =
  String


init : ( Model, Cmd Msg )
init =
  "Hello world" => Cmd.none



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
  div [] [ text model ]
