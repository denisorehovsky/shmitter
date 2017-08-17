module Page.Home exposing
  ( Model
  , init
  , Msg
  , update
  , view
  )

import Task exposing (Task)

import Html exposing (Html, div, text)
import Http

import Data.Token as Token exposing (Token)
import Data.User as User exposing (User)
import Page.Errored as Errored
import Request.User
import Utils exposing ((=>))


-- MODEL


type alias Model =
  { user : User
  }


init : Token -> Task Errored.Model Model
init token =
  let
    user =
      Request.User.fetchByToken token
        |> Http.toTask

    handlePageError _ =
      Errored.Model "Home page is currently unavailable"
  in
    Task.map Model user
      |> Task.mapError handlePageError



-- MESSAGES


type Msg
  = NoOp



-- UPDATE


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    NoOp ->
      model => Cmd.none



-- VIEW


view : Model -> Html Msg
view model =
  div [] [ text "Home page" ]
