require File.dirname(__FILE__) + '/../test_helper'
require 'digital_masters_controller'

# Re-raise errors caught by the controller.
class DigitalMastersController; def rescue_action(e) raise e end; end

class DigitalMastersControllerTest < Test::Unit::TestCase
  fixtures :contents_names

  def setup
    @controller = DigitalMastersController.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  def test_index
    get :index
    assert_response :success
    assert_template 'list'
  end

  def test_list
    get :list

    assert_response :success
    assert_template 'list'

    assert_not_nil assigns(:contents_names)
  end

  def test_show
    get :show, :id => 1

    assert_response :success
    assert_template 'show'

    assert_not_nil assigns(:contents_names)
    assert assigns(:contents_names).valid?
  end

  def test_new
    get :new

    assert_response :success
    assert_template 'new'

    assert_not_nil assigns(:contents_names)
  end

  def test_create
    num_contents_names = ContentsNames.count

    post :create, :contents_names => {}

    assert_response :redirect
    assert_redirected_to :action => 'list'

    assert_equal num_contents_names + 1, ContentsNames.count
  end

  def test_edit
    get :edit, :id => 1

    assert_response :success
    assert_template 'edit'

    assert_not_nil assigns(:contents_names)
    assert assigns(:contents_names).valid?
  end

  def test_update
    post :update, :id => 1
    assert_response :redirect
    assert_redirected_to :action => 'show', :id => 1
  end

  def test_destroy
    assert_not_nil ContentsNames.find(1)

    post :destroy, :id => 1
    assert_response :redirect
    assert_redirected_to :action => 'list'

    assert_raise(ActiveRecord::RecordNotFound) {
      ContentsNames.find(1)
    }
  end
end
