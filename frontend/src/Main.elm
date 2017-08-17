module Main exposing (..)

import Json.Encode exposing (Value)

import Html exposing (Html, div, text)
import Navigation exposing (Location)

import Data.Token as Token exposing (Token)
import Page.Errored as Errored
import Page.Home as Home
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
  | Errored Errored.Model
  | Home Home.Model
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
  | HomeMsg Home.Msg
  | LoginMsg Login.Msg


setRoute : Maybe Route -> Model -> ( Model, Cmd Msg )
setRoute maybeRoute model =
  case maybeRoute of
    Nothing ->
      { model | page = NotFound }
        => Cmd.none

    Just Route.Home ->
      case model.token of
        Nothing ->
          model
            => Route.modifyUrl Route.Login

        Just token ->
          { model | page = Home { user = "HAHA USER" } }
            => Cmd.none

    Just Route.Login ->
      { model | page = Login Login.initialModel }
        => Cmd.none

    Just Route.Logout ->
      { model | token = Nothing }
        => Cmd.batch
          [ Ports.storeToken Nothing
          , Route.modifyUrl Route.Home
          ]


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case ( msg, model.page ) of
    ( SetRoute maybeRoute, _ ) ->
      setRoute maybeRoute model

    ( HomeMsg subMsg, Home subModel ) ->
      let
        ( newHomeModel, cmd )
          = Home.update subMsg subModel
      in
        { model | page = Home newHomeModel }
          => Cmd.map HomeMsg cmd

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

    Errored subModel ->
      Errored.view subModel

    Home subModel ->
      Home.view subModel
        |> Html.map HomeMsg

    Login subModel ->
      Login.view subModel
        |> Html.map LoginMsg
