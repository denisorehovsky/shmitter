module Main exposing (..)

import Json.Encode exposing (Value)
import Task

import Html exposing (Html, div, text)
import Navigation exposing (Location)

import Data.Token as Token exposing (Token)
import Page.Errored as Errored
import Page.Home as Home
import Page.NotFound as NotFound
import Page.Signin as Signin
import Ports
import Route exposing (Route)
import Utils exposing ((=>))
import View.Navbar as Navbar


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
  | Signin Signin.Model


type alias Model =
  { navbar : Navbar.Model
  , page : Page
  , token : Maybe Token
  }


initialPage : Page
initialPage =
  Blank


init : Value -> Location -> ( Model, Cmd Msg )
init value location =
  setRoute (Route.parseLocation location)
    { navbar = Navbar.initialModel
    , page = initialPage
    , token = Token.decodeTokenFromJson value
    }



-- MESSAGES


type Msg
  = SetRoute (Maybe Route)
  | NavbarMsg Navbar.Msg
  | HomeLoaded (Result Errored.Model Home.Model)
  | HomeMsg Home.Msg
  | SigninMsg Signin.Msg



-- UPDATE


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
            => Route.modifyUrl Route.Signin

        Just token ->
          model
            => Task.attempt HomeLoaded (Home.init token)

    Just Route.Signin ->
      { model | page = Signin Signin.initialModel }
        => Cmd.none

    Just Route.Signout ->
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

    ( NavbarMsg subMsg, _ ) ->
      let
        ( newNavbarModel, cmd )
          = Navbar.update subMsg model.navbar
      in
        { model | navbar = newNavbarModel }
          => Cmd.map NavbarMsg cmd

    ( HomeLoaded (Ok subModel), _ ) ->
      { model | page = Home subModel }
        => Cmd.none

    ( HomeLoaded (Err erroredModel), _ ) ->
      { model | page = Errored erroredModel }
        => Cmd.none

    ( HomeMsg subMsg, Home subModel ) ->
      let
        ( newHomeModel, cmd )
          = Home.update subMsg subModel
      in
        { model | page = Home newHomeModel }
          => Cmd.map HomeMsg cmd

    ( SigninMsg subMsg, Signin subModel ) ->
      let
        ( ( newSigninModel, cmd ), msgFromSignin ) =
          Signin.update subMsg subModel

        newModel =
          case msgFromSignin of
            Signin.NoOp ->
              model

            Signin.SetToken token ->
              { model | token = Just token }
      in
        { newModel | page = Signin newSigninModel }
          => Cmd.map SigninMsg cmd

    ( _, NotFound ) ->
      model => Cmd.none

    ( _, _ ) ->
      model => Cmd.none



-- VIEW


view : Model -> Html Msg
view model =
  let
    frame activePage content =
      div []
        [ Html.map NavbarMsg (Navbar.view model.navbar activePage)
        , content
        ]
  in
    case model.page of
      Blank ->
        Html.text "Blank"

      NotFound ->
        NotFound.view
          |> frame Navbar.None

      Errored subModel ->
        Errored.view subModel
          |> frame Navbar.None

      Home subModel ->
        Home.view subModel
          |> Html.map HomeMsg
          |> frame Navbar.Home

      Signin subModel ->
        Signin.view subModel
          |> Html.map SigninMsg
