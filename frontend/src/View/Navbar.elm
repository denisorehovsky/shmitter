module View.Navbar exposing
  ( ActivePage(..)
  , Model
  , initialModel
  , Msg
  , update
  , view
  )

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)

import Route exposing (Route)
import Utils exposing ((=>))


-- MODEL


type ActivePage
  = None
  | Home
  | Logout


type LinkFor
  = All
  | Mobile
  | Tablet


type alias Model =
  { showMobileMenu : Bool
  }


initialModel : Model
initialModel =
  { showMobileMenu = False
  }



-- MESSAGES


type Msg
  = ToggleMobileMenu



-- UPDATE


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    ToggleMobileMenu ->
      { model | showMobileMenu = not model.showMobileMenu }
        => Cmd.none



-- VIEW


view : Model -> ActivePage -> Html Msg
view model activePage =
  div [ class "container" ]
    [ nav [ class "nav has-shadow" ]
      [ div [ class "container" ]
        [ div [ class "nav-left" ]
          [ navbarLink Route.Home (activePage == Home) Tablet [ text "Home" ]
          ]
        , div [ class "nav-center" ]
          [ viewLogo
          ]
        , span [ onClick ToggleMobileMenu, class "nav-toggle" ]
          [ span [] []
          , span [] []
          , span [] []
          ]
        , div [ class "nav-right nav-menu"
              , classList [ ("is-active", model.showMobileMenu) ]
              ]
          [ navbarLink Route.Home (activePage == Home) Mobile [ text "Home" ]
          , a [ class "nav-item is-tab", href "" ]
            [ figure [ class "image is-16x16 mr1" ]
              [ img [ alt "", src "http://bulma.io/images/jgthms.png" ]
                []
              ]
            , text "Profile"
            ]
          , navbarLink Route.Logout (activePage == Logout) All [ text "Log out" ]
          ]
        ]
      ]
    ]


viewLogo : Html msg
viewLogo =
  a [ class "nav-item", Route.href Route.Home ]
    [ img [ alt "Shmitter", src "http://bulma.io/images/bulma-logo.png" ]
      []
    ]


navbarLink : Route -> Bool -> LinkFor -> List (Html msg) -> Html msg
navbarLink route isActive linkFor linkContent =
  a [ class "nav-item is-tab"
    , classList [ ("is-active", isActive)
                , ("is-hidden-mobile", linkFor == Tablet)
                , ("is-hidden-tablet", linkFor == Mobile)
                ]
    , Route.href route
    ]
    linkContent
