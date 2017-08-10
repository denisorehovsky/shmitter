module Main exposing (..)

import Html exposing (Html, div, text)
import Navigation exposing (Location)

import Route exposing (Route)
import Utils exposing ((=>))


main : Program Never Model Msg
main =
  Navigation.program (Route.parseLocation >> SetRoute)
    { init = init
    , view = view
    , update = update
    , subscriptions = \_ -> Sub.none
    }



-- MODEL


type Page
  = Blank
  | NotFound
  | Home
  | Login


type alias Model =
  { page : Page
  }


initialPage : Page
initialPage =
  Blank


init : Location -> ( Model, Cmd Msg )
init location =
  setRoute (Route.parseLocation location)
    { page = initialPage
    }



-- UPDATE


type Msg
  = SetRoute (Maybe Route)


setRoute : Maybe Route -> Model -> ( Model, Cmd Msg )
setRoute maybeRoute model =
  case maybeRoute of
    Nothing ->
      { model | page = NotFound }
        => Cmd.none

    Just Route.Home ->
      { model | page = Home }
        => Cmd.none

    Just Route.Login ->
      { model | page = Login }
        => Cmd.none


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case ( msg, model.page ) of
    ( SetRoute maybeRoute, _ ) ->
      setRoute maybeRoute model



-- VIEW


view : Model -> Html Msg
view model =
  case model.page of
    Blank ->
      Html.text "Blank"

    NotFound ->
      Html.text "Not found"

    Home ->
      Html.text "Home"

    Login ->
      Html.text "Login"
