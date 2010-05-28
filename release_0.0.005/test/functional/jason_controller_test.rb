require File.dirname(__FILE__) + '/../test_helper'
require 'jason_controller'

# Re-raise errors caught by the controller.
class JasonController; def rescue_action(e) raise e end; end

class JasonControllerTest < Test::Unit::TestCase
  fixtures :src_still_images

  def setup
    @controller = JasonController.new
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

    assert_not_nil assigns(:src_still_images)
  end

  def test_show
    get :show, :id => 1

    assert_response :success
    assert_template 'show'

    assert_not_nil assigns(:src_still_image)
    assert assigns(:src_still_image).valid?
  end

  def test_new
    get :new

    assert_response :success
    assert_template 'new'

    assert_not_nil assigns(:src_still_image)
  end

  def test_create
    num_src_still_images = SrcStillImage.count

    post :create, :src_still_image => {}

    assert_response :redirect
    assert_redirected_to :action => 'list'

    assert_equal num_src_still_images + 1, SrcStillImage.count
  end

  def test_edit
    get :edit, :id => 1

    assert_response :success
    assert_template 'edit'

    assert_not_nil assigns(:src_still_image)
    assert assigns(:src_still_image).valid?
  end

  def test_update
    post :update, :id => 1
    assert_response :redirect
    assert_redirected_to :action => 'show', :id => 1
  end

  def test_destroy
    assert_not_nil SrcStillImage.find(1)

    post :destroy, :id => 1
    assert_response :redirect
    assert_redirected_to :action => 'list'

    assert_raise(ActiveRecord::RecordNotFound) {
      SrcStillImage.find(1)
    }
  end
end
