module Main exposing (..)

import Json.Encode exposing (Value)

import Html exposing (Html, div, text)
import Navigation exposing (Location)

import Data.Token as Token exposing (Token)
import Page.Login as Login
import Ports
import Route exposing (Route)
import Utils exposing ((=>))


main : Program Value Model Msg
main =
  Navigation.programWithFlags (Route.parseLocation >> SetRoute)
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
  | Login Login.Model


type alias Model =
  { page : Page
  , token : Maybe Token
  }


initialPage : Page
initialPage =
  Blank


init : Value -> Location -> ( Model, Cmd Msg )
init value location =
  setRoute (Route.parseLocation location)
    { page = initialPage
    , token = Token.decodeTokenFromJson value
    }



-- UPDATE


type Msg
  = SetRoute (Maybe Route)
  | LoginMsg Login.Msg


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
      { model | page = Login Login.initialModel }
        => Cmd.none


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case ( msg, model.page ) of
    ( SetRoute maybeRoute, _ ) ->
      setRoute maybeRoute model

    ( LoginMsg subMsg, Login subModel ) ->
      let
        ( ( newLoginModel, cmd ), msgFromLogin ) =
          Login.update subMsg subModel

        newModel =
          case msgFromLogin of
            Login.NoOp ->
              model

            Login.SetToken token ->
              { model | token = Just token }
      in
        { newModel | page = Login newLoginModel }
          => Cmd.map LoginMsg cmd

    ( _, NotFound ) ->
      model => Cmd.none

    ( _, _ ) ->
      model => Cmd.none



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

    Login subModel ->
      Login.view subModel
        |> Html.map LoginMsg
