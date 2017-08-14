module Page.Login exposing
  ( Model
  , initialModel
  , Msg
  , ExternalMsg(..)
  , update
  , view
  )

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onSubmit)
import Http

import Data.Token as Token exposing (Token)
import Request.Token
import Utils exposing ((=>))


-- MODEL


type alias Model =
  { usernameOrEmail : String
  , password : String
  }


initialModel : Model
initialModel =
  { usernameOrEmail = ""
  , password = ""
  }



-- UPDATE


type Msg
  = SubmitForm
  | SetUsernameOrEmail String
  | SetPassword String
  | TokenObtained (Result Http.Error Token)


type ExternalMsg
  = NoOp
  | SetToken Token


update : Msg -> Model -> ( ( Model, Cmd Msg ), ExternalMsg )
update msg model =
  case msg of
    SubmitForm ->
      model
        => Http.send TokenObtained (Request.Token.obtain model)
        => NoOp

    SetUsernameOrEmail usernameOrEmail ->
      { model | usernameOrEmail = usernameOrEmail }
        => Cmd.none
        => NoOp

    SetPassword password ->
      { model | password = password }
        => Cmd.none
        => NoOp

    TokenObtained (Ok token) ->
      model
        => Token.storeToken token
        => SetToken token

    TokenObtained (Err _) ->
      model
        => Cmd.none
        => NoOp



-- VIEW


view : Model -> Html Msg
view model =
  section [ class "section" ]
    [ div [ class "container" ]
      [ div [ class "columns" ]
        [ div [ class "column is-one-third" ]
          []
        , div [ class "column" ]
          [ div [ class "card" ]
            [ Html.form [ onSubmit SubmitForm ]
              [ div [ class "card-content" ]
                [ div [ class "content" ]
                  [ div [ class "field" ]
                    [ p [ class "control" ]
                      [ input [ onInput SetUsernameOrEmail, class "input", placeholder "Username or email", type_ "text" ]
                        []
                      ]
                    ]
                  , div [ class "field has-addons" ]
                    [ p [ class "control is-expanded" ]
                      [ input [ onInput SetPassword, class "input", placeholder "Password", type_ "password" ]
                        []
                      ]
                    , p [ class "control" ]
                      [ a [ class "button" ]
                        [ text "Forgot?" ]
                      ]
                    ]
                  ]
                , footer [ class "card-footer" ]
                  [ a [ class "card-footer-item" ]
                    [ button [ class "button is-success", type_ "submit" ]
                      [ text "Log in" ]
                    ]
                  ]
                ]
              ]
            ]
          , div [ class "content has-text-centered mt4" ]
            [ p []
              [ text "Don't have an account? "
              , a [ href "#/signup" ]
                [ text "Sign up" ]
              ]
            ]
          ]
        , div [ class "column is-one-third" ]
          []
        ]
      ]
    ]
